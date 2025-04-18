import json
import time
import os
import logging # Added standard logging
import threading
from flask import Flask, request, jsonify
import google.auth # Added for ADC
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from googleapiclient.discovery import build, Resource
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session, GetSessionConfig
from google.genai import types as genai_types
from google.adk.agents import LlmAgent
from typing import Callable, List, Any, Dict, Optional

# --- Logging Configuration ---
# Configure logging to output to stdout/stderr, which Cloud Run captures
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# ---

# Define a type hint for the agent generation function
AgentGenerator = Callable[[str, str, Callable], LlmAgent]

class GoogleChatBot:
    """
    Handles Google Chat events received via HTTP webhook for Cloud Run.
    Manages sessions, agents, and interacts with the Google Chat API using ADC.
    Uses standard Python logging.
    """

    def __init__(self,
                 generate_agent_fn: AgentGenerator,
                 chat_service: Resource, # Pass the authenticated Chat API service
                 allowed_space_ids: List[str] = [], # Use Chat space IDs (space.name)
                 app_name: str = "GoogleChatBot",
                 session_size: int = -1):
        self.generate_agent_fn = generate_agent_fn
        self.allowed_space_ids = allowed_space_ids
        self.chat_service = chat_service # Store the Chat API client
        self.runners: Dict[str, Runner] = {}
        self.session_service = InMemorySessionService()
        self.app_name = app_name
        # Lock for thread-safe access to runners dictionary during creation
        self.runner_lock = threading.Lock()
        self.session_size = session_size

    def _create_send_chat_message_tool(self, space_name: str) -> Callable:
        """
        Factory function to create the tool for sending a message
        back to a specific Google Chat space.
        """
        def send_reply_to_user(msg: str) -> str:
            """
            Use this tool to send a message text back to the user. You MUST use this tool for sending the message.
            Args:
                msg: The text content of the message to send.
            """
            logging.info(f"Agent requested sending message via tool to space {space_name}")
            # Use logging.debug for potentially verbose output
            # logging.debug(f"Message content: {message_text}")
            try:
                message_body = {'text': msg}
                self.chat_service.spaces().messages().create(
                    parent=space_name,
                    body=message_body
                ).execute()
                return "DONE"
            except Exception as e:
                logging.error(f"Error sending message via tool to space {space_name}: {e}", exc_info=True)
                return f"Error sending message: {e}"
        return send_reply_to_user

    def _process_event_async(self, chat_event: Dict[str, Any]):
        """
        Internal method to process the chat event in a background thread.
        """
        try:
            # Use logging.debug for verbose event logging
            logging.debug(f"--- Received Event ---\n{json.dumps(chat_event, indent=2)}\n--------------------")

            event_type = chat_event.get('type')

            if event_type == 'ADDED_TO_SPACE':
                 space_info = chat_event.get('space', {})
                 logging.info(f"Bot added to space: {space_info.get('name')} (Type: {space_info.get('type')})")
                 # Optional: Send welcome message
                 # space_name = space_info.get('name')
                 # if space_name:
                 #    try:
                 #       self.chat_service.spaces().messages().create(parent=space_name, body={'text': "Thanks for adding me!"}).execute()
                 #       logging.info(f"Sent welcome message to {space_name}")
                 #    except Exception as e:
                 #       logging.error(f"Error sending welcome message to {space_name}: {e}", exc_info=True)
                 return
            elif event_type == 'REMOVED_FROM_SPACE':
                space_name = chat_event.get('space', {}).get('name')
                logging.info(f"Bot removed from space: {space_name}")
                if space_name:
                    with self.runner_lock:
                        if space_name in self.runners:
                            del self.runners[space_name]
                            logging.info(f"Removed runner cache for space {space_name}")
                return

            if event_type != 'MESSAGE':
                logging.debug(f"Ignoring event type: {event_type}")
                return

            chat_message = chat_event.get('message')
            space = chat_event.get('space')
            user = chat_event.get('user')

            if not chat_message or not space or not user or not chat_message.get('text'):
                logging.warning("Ignoring event with missing message/space/user/text data.")
                return

            sender = chat_message.get('sender')
            if not sender or sender.get('type') != 'HUMAN':
                 logging.debug(f"Ignoring message from non-human sender: {sender.get('type') if sender else 'Unknown'}")
                 return

            space_name = space.get('name')
            user_name = user.get('name')
            message_text = chat_message.get('argumentText', chat_message.get('text', '')).strip()

            if not space_name or not user_name or not message_text:
                 logging.warning("Ignoring event with missing space name, user name, or text content.")
                 return

            # --- Authorization ---
            if self.allowed_space_ids and space_name not in self.allowed_space_ids:
                logging.info(f"Space {space_name} is restricted. Ignoring message.")
                try:
                    self.chat_service.spaces().messages().create(
                        parent=space_name,
                        body={'text': "Sorry, this bot is not enabled for this space."}
                    ).execute()
                except Exception as e:
                    logging.error(f"Error sending restriction message to {space_name}: {e}", exc_info=True)
                return

            # --- Session Management ---
            adk_user_id = user_name
            adk_session_id = space_name

            try:
                chat_session: Session = self.session_service.get_session(
                    app_name=self.app_name,
                    user_id=adk_user_id,
                    session_id=adk_session_id,
                    config=GetSessionConfig(num_recent_events=10))
                if not chat_session:
                    logging.info(f"Creating new session for user {adk_user_id} in space {adk_session_id}")
                    chat_session = self.session_service.create_session(
                        app_name=self.app_name,
                        user_id=adk_user_id,
                        session_id=adk_session_id)
            except Exception as e:
                logging.error(f"Error managing session for space {adk_session_id}: {e}", exc_info=True)
                try:
                    self.chat_service.spaces().messages().create(
                        parent=space_name,
                        body={'text': "Sorry, there was a session error. Please try again."}
                    ).execute()
                except Exception as e_inner:
                     logging.error(f"Error sending session error message to {space_name}: {e_inner}", exc_info=True)
                return

            # --- Runner and Agent Creation (Thread-Safe) ---
            runner_instance = self.runners.get(adk_session_id)
            if not runner_instance:
                with self.runner_lock:
                    runner_instance = self.runners.get(adk_session_id) # Double-check
                    if not runner_instance:
                        logging.info(f"Creating new Runner/Agent for space {adk_session_id}")
                        try:
                            send_message_tool = self._create_send_chat_message_tool(space_name)
                            agent = self.generate_agent_fn(
                                user_name=user_name,
                                space_name=space_name,
                                send_google_chat_message=send_message_tool
                            )

                            if not isinstance(agent, LlmAgent):
                                # Raise error instead of just logging for critical failures
                                raise TypeError("generate_agent_fn did not return an LlmAgent instance.")

                            runner_instance = Runner(
                                agent=agent,
                                app_name=self.app_name,
                                session_service=self.session_service
                            )
                            self.runners[adk_session_id] = runner_instance
                        except Exception as e:
                            logging.exception(f"Fatal Error creating agent/runner for space {adk_session_id}: {e}") # Use exception for traceback
                            try:
                                self.chat_service.spaces().messages().create(
                                    parent=space_name,
                                    body={'text': "Sorry, failed to initialize the agent. Please contact support."}
                                ).execute()
                            except Exception as e_inner:
                                logging.error(f"Error sending agent init error message to {space_name}: {e_inner}", exc_info=True)
                            return

            # --- Process Message with Runner ---
            logging.info(f"Processing message from user {adk_user_id} in space {adk_session_id}")
            user_content = genai_types.Content(role='user', parts=[genai_types.Part(text=message_text)])
            final_response_text = ""

            try:
                for event in runner_instance.run(
                    user_id=adk_user_id,
                    new_message=user_content,
                    session_id=adk_session_id):

                    logging.debug(f"ADK Event ({adk_session_id}): Author={event.author}, Content={event.content}")

                    if event.error_message:
                        logging.error(f"ADK Runner Error ({adk_session_id}): {event.error_message}")
                        break

                    if event.is_final_response() and event.content and event.content.parts:
                        text_part = next((part.text for part in event.content.parts if part.text), None)
                        if text_part:
                            final_response_text = text_part
                            logging.debug(f"ADK signaled final response with text ({adk_session_id}): {final_response_text}")
                        break
            except Exception as e:
                 logging.exception(f"Error during runner.run for space {adk_session_id}: {e}")
                 # Optionally inform user about processing error via the tool
                 try:
                    send_message_tool = self._create_send_chat_message_tool(space_name)
                    send_message_tool("Sorry, an error occurred while processing your request with the agent.")
                 except Exception as e_inner:
                    logging.error(f"Failed to send runner error message to user in {space_name}: {e_inner}", exc_info=True)

            logging.info(f"Runner loop finished for space {adk_session_id}.")
            if final_response_text:
                    logging.debug(f"Note: ADK provided final text for space {adk_session_id}, "
                        "but relying on agent to use send_chat_message_tool for output.")

        except Exception as e:
            logging.exception(f"Unexpected error processing chat event: {e}") # Log with traceback
            try:
                space_name = chat_event.get('space', {}).get('name')
                if space_name:
                     self.chat_service.spaces().messages().create(
                        parent=space_name,
                        body={'text': "Sorry, an unexpected error occurred while processing your message."}
                    ).execute()
            except Exception as e_inner:
                logging.error(f"Error sending unexpected error message: {e_inner}", exc_info=True)

    # --- HTTP Request Handler ---
    def handle_chat_event(self, request_data: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Handles the incoming HTTP POST request containing the chat event.
        Verifies token (placeholder) and starts processing in a background thread.
        Returns an immediate response to Google Chat.
        """
        # --- Bearer Token Verification (Conceptual - Adapt for Production) ---
        # In Cloud Run, you might configure Cloud IAM Invoker roles and rely on
        # Google Cloud's infrastructure for authentication, or use Identity Platform/IAP.
        # If using the standard Bearer token from Chat API:
        auth_header = headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logging.warning("Missing or invalid Authorization header")
            # IMPORTANT: In a real app, return 401 Unauthorized here.
            # For now, we'll proceed but log the warning.
            return jsonify({"error": "Unauthorized"}), 401
        else:
            try:
                # TODO: Implement actual token verification using google.oauth2.id_token.verify_oauth2_token
                # You need the Audience (often the Cloud Run service URL or project number)
                audience = os.environ.get("ID_TOKEN_AUDIENCE") # Configure this env var
                if audience:
                   id_info = id_token.verify_oauth2_token(id_token, Request(), audience=audience)
                   logging.info(f"Successfully verified token for issuer: {id_info.get('iss')}")
                else:
                   logging.warning("ID_TOKEN_AUDIENCE environment variable not set. Skipping token verification.")
                logging.debug("Skipping token verification (placeholder).") # Placeholder
                pass # Placeholder for successful verification
            except ValueError as e:
                logging.error(f"Invalid token received: {e}")
                # IMPORTANT: In a real app, return 401 Unauthorized here.
                # return jsonify({"error": "Invalid token"}), 401
            except Exception as e:
                 logging.exception(f"Error during token verification: {e}")
                 # IMPORTANT: In a real app, return 500 Internal Server Error here.
                 # return jsonify({"error": "Token verification failed"}), 500

        chat_event = request_data
        processing_thread = threading.Thread(target=self._process_event_async, args=(chat_event,))
        processing_thread.start()
        return {} # Acknowledge async processing

# --- Flask App Setup ---
flask_app = Flask(__name__)
google_chat_bot_instance = None # Global variable

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint to receive Google Chat events."""
    if not google_chat_bot_instance:
        logging.error("Webhook called before Bot instance is initialized.")
        return jsonify({"error": "Bot not configured"}), 500

    try:
        request_json = request.get_json()
        if not request_json:
            logging.warning("Received empty request data.")
            return jsonify({"error": "Bad Request"}), 400

        # Pass headers for potential token verification
        response_body = google_chat_bot_instance.handle_chat_event(request_json, request.headers)
        return jsonify(response_body), 200

    except Exception as e:
        logging.exception("Error in webhook handler") # Log full traceback
        return jsonify({"error": "Internal Server Error"}), 500

# --- Authentication Function (Removed - Using ADC now) ---
# def authenticate_google_cloud(...)

# --- start_chat_webhook_server function ---
def start_chat_webhook_server(*,
                              host: str = '0.0.0.0',
                              port: int = 8080,
                              allowed_space_ids: List[str] = None,
                              generate_agent_fn: AgentGenerator,
                              app_name: str = "GoogleChatBot"):
    global google_chat_bot_instance

    chat_scopes = [
        'https://www.googleapis.com/auth/chat.messages.create',
        'https://www.googleapis.com/auth/chat.messages.readonly',
        'https://www.googleapis.com/auth/chat.spaces.readonly',
        'https://www.googleapis.com/auth/chat.memberships.readonly',
    ]

    # 1. Authenticate using Application Default Credentials (ADC)
    try:
        logging.info("Attempting authentication using Application Default Credentials...")
        credentials, project_id = google.auth.default(scopes=chat_scopes)
        # Optionally refresh credentials if needed, though ADC usually handles this
        # credentials.refresh(Request())
        logging.info(f"Successfully obtained ADC credentials. Project ID: {project_id or 'Not determined'}")
        chat_service = build('chat', 'v1', credentials=credentials, cache_discovery=False)
        logging.info("Google Chat service client built successfully.")
    except Exception as e:
        logging.exception("Failed to authenticate using ADC or build Google Chat service.")
        return # Exit if authentication fails

    # 2. Instantiate the Bot wrapper class (pass debug=False)
    google_chat_bot_instance = GoogleChatBot(
        generate_agent_fn=generate_agent_fn,
        chat_service=chat_service,
        allowed_space_ids=allowed_space_ids or [],
        app_name=app_name
        # debug parameter removed
    )
    logging.info(f"GoogleChatBot instance created for app: {app_name}")

    # 3. Start the Flask web server (without debug mode for production)
    logging.info(f"Starting Google Chat HTTP webhook listener on http://{host}:{port}/webhook")
    if allowed_space_ids:
        logging.info(f"Restricted to spaces: {allowed_space_ids}")
    else:
        logging.info("Not restricted to specific spaces.")

    # Use a production-ready WSGI server in a real Cloud Run deployment
    # (e.g., gunicorn, waitress). Flask's development server is used here
    # for simplicity, but set debug=False explicitly.
    # The Dockerfile for Cloud Run should use gunicorn or similar.
    # Example Dockerfile CMD: CMD ["gunicorn", "--bind", "0.0.0.0:8080", "your_module:flask_app"]
    flask_app.run(host=host, port=port, debug=False)
