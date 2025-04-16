import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import pprint
import os

from flask import Request, jsonify

# Logging configuration
log_level = getattr(logging, os.environ.get('LOG_LEVEL', 'DEBUG').upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logging.getLogger('watchdog').setLevel(logging.INFO) # Silence specific loggers
logger = logging.getLogger(__name__) # Main logger


class GChatbot(ABC):
    """
    Base class for creating Google Chat bots.

    Provides a foundational structure for handling incoming HTTP requests
    from Google Chat, parsing event data, extracting key information,
    and routing events to appropriate processing methods.

    Subclasses should implement the abstract methods `_process_slash_command`
    and `_process_message` to define the bot's specific logic for handling
    slash commands and direct messages respectively.
    """

    def __init__(self, bot_name: str = "GoogleChatBot", bot_image: str = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaF5_rrfPgOGVnxvd54FKhwmCR54sGaOJTUw&s"):
        """
        Initializes the base bot.

        Args:
            bot_name: The name of the bot, used for mentions. Defaults to "GoogleChatBot".
            bot_image: The URL for the bot's avatar image. Defaults to a generic bot icon.
        """
        self.bot_name = bot_name
        self.bot_image = bot_image
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"{self.__class__.__name__} initialized.")

    def handle_request(self, request: Request) -> Any:
        """
        Main entry point for handling HTTP requests from Google Chat.

        Args:
            request: The Flask request object containing the event data.

        Returns:
            A JSON response suitable for Google Chat API, or an error message.
        """
        if request.method == 'GET':
            # Basic check or landing page for GET requests
            return f"{self.bot_name} is active. Use it in a Google Chat space."

        if request.method != 'POST':
            self.logger.warning(f"Received unsupported HTTP method: {request.method}")
            return jsonify({"error": "Method not allowed"}), 405

        # Process POST request containing event data
        try:
            event_data = request.get_json(silent=True)
            if not event_data:
                self.logger.error("Empty or invalid JSON payload received.")
                # Return an empty response for certain event types Google sends
                return jsonify({})
            self.logger.debug(f"Received event data:\n {pprint.pformat(event_data)}")

            # Extract key information from the event
            extracted_data = self._extract_event_data(event_data)
            if not extracted_data:
                self.logger.warning("Could not extract necessary data from the event.")
                return jsonify({}) # Or potentially an error message

            # Process the event based on extracted data
            response_text = self._process_event(extracted_data, event_data)

            # Format and return the response
            return self._format_response(response_text, event_data)

        except Exception as e:
            self.logger.exception(f"Error handling request: {e}")
            # Return a generic error message to Google Chat
            error_response = {"text": "An internal error occurred while processing your request."}
            return jsonify(error_response)


    def _extract_event_data(self, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extracts relevant information from the Google Chat event payload.

        Handles variations in payload structure (e.g., direct vs. wrapped in 'chat').

        Args:
            event_data: The parsed JSON payload from the Google Chat event.

        Returns:
            A dictionary containing extracted data (text, command, args, user_email,
            space_name, is_direct_message) or None if essential data is missing.
        """
        try:
            # Determine the source of the message payload
            if 'chat' in event_data and 'messagePayload' in event_data['chat']:
                payload = event_data['chat']['messagePayload']
                user = event_data['chat'].get('user', {})
                message = payload.get('message', {})
                space = message.get('space', {})
                is_direct_message_event = False # Event comes from Chat App API
            elif 'message' in event_data: # Standard message event
                payload = event_data # Simplified structure
                user = event_data.get('user', {})
                message = event_data.get('message', {})
                space = event_data.get('space', {})
                is_direct_message_event = True # Assume direct if not through Chat App API structure
            else:
                 self.logger.warning(f"Unrecognized event structure: {event_data.keys()}")
                 return None

            # Extract common fields
            text = message.get('argumentText') or message.get('text', '')
            text = text.strip() if text else ''
            user_email = user.get('email', 'Unknown Email')
            space_name = space.get('name', 'Unknown Space')
            user_display_name = user.get('displayName', 'Unknown User')

            command = None
            arguments = text # Default arguments are the full text for messages

            # Handle mentions and potential slash commands
            mention_trigger = f"@{self.bot_name}"
            if text.startswith(mention_trigger):
                text = text[len(mention_trigger):].strip()
                arguments = text # Update arguments after removing mention

            if text.startswith('/'):
                parts = text[1:].split(" ", 1)
                command = parts[0].lower()
                arguments = parts[1].strip() if len(parts) > 1 else ''

            extracted = {
                "raw_text": message.get('text', '').strip(), # Original text if needed
                "processed_text": text, # Text after removing mention/command prefix
                "command": command,
                "arguments": arguments,
                "user_email": user_email,
                "user_display_name": user_display_name,
                "space_name": space_name,
                "is_direct_message_event": is_direct_message_event
            }
            self.logger.info(f"Extracted data:\n {pprint.pformat(extracted)}")
            return extracted

        except Exception as e:
            self.logger.exception(f"Error extracting data from event: {e} - Event Data: {event_data}")
            return None

    def _process_event(self, extracted_data: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """
        Routes the event to the appropriate handler based on extracted data.

        Args:
            extracted_data: The dictionary of data extracted by `_extract_event_data`.
            event_data: The original event payload (passed for context if needed).

        Returns:
            The response text generated by the specific handler.
        """
        command = extracted_data.get("command")
        arguments = extracted_data.get("arguments", "")
        processed_text = extracted_data.get("processed_text", "")

        if command:
            self.logger.info(f"Processing slash command: /{command} with args: '{arguments}'")
            return self._process_slash_command(command, arguments, extracted_data, event_data)
        else:
            self.logger.info(f"Processing message: '{processed_text}'")
            return self._process_message(processed_text, extracted_data, event_data)

    @abstractmethod
    def _process_slash_command(self, command: str, arguments: str, extracted_data: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """
        Abstract method to handle recognized slash commands.
        Subclasses MUST implement this method to define command logic.

        Args:
            command: The name of the slash command (e.g., 'help').
            arguments: The arguments provided after the command name.
            extracted_data: The dictionary of data extracted from the event.
            event_data: The original event payload.

        Returns:
            The text response to send back to the chat.
        """
        # Example implementation in subclass:
        # if command == 'help':
        #     return "This is the help text."
        # else:
        #     return f"Unknown command: /{command}"
        raise NotImplementedError("Subclasses must implement _process_slash_command")

    @abstractmethod
    def _process_message(self, text: str, extracted_data: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """
        Abstract method to handle regular messages (not slash commands).
        Subclasses MUST implement this method to define message response logic.

        Args:
            text: The processed text of the message (mention removed).
            extracted_data: The dictionary of data extracted from the event.
            event_data: The original event payload.

        Returns:
            The text response to send back to the chat.
        """
        # Example implementation in subclass:
        # if "hello" in text.lower():
        #     return f"Hello {extracted_data['user_display_name']}!"
        # else:
        #     return "I received your message."
        raise NotImplementedError("Subclasses must implement _process_message")

    def _format_response(self, response_text: str, event_data: Dict[str, Any]) -> Any:
        """
        Formats the response into the JSON structure expected by Google Chat API.

        This method creates different response structures based on the event source:
        - For events with 'chat' key: Uses 'hostAppDataAction' structure required by 
        Google Workspace hosted apps, which need additional context for proper routing.
        - For direct messages/webhooks: Uses a simpler structure with just 'cardsV2'.

        Both formats deliver the same visual card to users, but follow different 
        routing paths through Google's infrastructure based on the app's integration type.

        Args:
            response_text: The text content to be displayed in the card.
            event_data: The original event payload from Google Chat, used to determine 
                    the appropriate response format.

        Returns:
            A Flask JSON response object with the properly formatted payload.
        """
        # Helper function to create the card structure
        def create_card():
            """
            Creates a card structure for the response.
            
            Returns:
                dict: The card structure with formatted content.
            """
            # Determine user based on event type
            user_display = (event_data.get('chat', {}).get('user', {}) 
                            if 'chat' in event_data else event_data.get('user', {}))
            
            return {
                "cardId": "responseCard",
                "card": {
                    "header": {
                        "title": self.bot_name,
                        "subtitle": f"Para: {user_display.get('displayName', 'Usuário')}",
                        "imageUrl": self.bot_image,
                        "imageType": "CIRCLE",
                        "imageAltText": self.bot_name
                    },
                    "sections": [{
                        "widgets": [{
                            "textParagraph": {
                                "text": response_text
                            }
                        }]
                    }]
                }
            }
        
        # Build payload based on event type
        if 'chat' in event_data:
            # Format for Chat App API events
            response_payload = {
                "hostAppDataAction": {
                    "chatDataAction": {
                        "createMessageAction": {
                            "message": {
                                "cardsV2": [create_card()]
                            }
                        }
                    }
                }
            }
        else:
            # Format for direct messages/webhooks
            response_payload = {"cardsV2": [create_card()]}
        
        self.logger.debug(f"Sending response payload:\n {pprint.pformat(response_payload)}")
        return jsonify(response_payload)