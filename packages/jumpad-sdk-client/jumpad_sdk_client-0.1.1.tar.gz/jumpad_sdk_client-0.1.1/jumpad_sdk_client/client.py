import requests
import json
from typing import Dict, Any, Optional, List, Union
import time

class LLMAgentError(Exception):
    """Custom exception for LLM Agent SDK errors."""
    def __init__(self, status_code: int, error_message: str, response_body: Optional[Any] = None):
        self.status_code = status_code
        self.error_message = error_message
        self.response_body = response_body
        super().__init__(f"SDK Error {status_code}: {error_message}")

class ConversationTracker:
    """
    Helper class to track messages exchanged during a conversation.
    This is useful when the SDK doesn't reliably return the complete message history.
    Automatically prevents duplicate messages from being added.
    """
    def __init__(self):
        self.conversations = {}  # chat_id -> list of messages
        
    def add_message(self, chat_id: str, message: Dict[str, Any]):
        """
        Add a message to the tracked conversation, preventing duplicates.
        A message is considered a duplicate if an existing message has the same message_type and content.
        """
        if chat_id not in self.conversations:
            self.conversations[chat_id] = []
        
        # Check for duplicates before adding
        should_add = True
        msg_type = message.get('message_type')
        msg_content = message.get('message')
        
        if msg_type and msg_content:
            # Only check for duplicates if the message has both type and content
            for existing_msg in self.conversations[chat_id]:
                if (existing_msg.get('message_type') == msg_type and 
                    existing_msg.get('message') == msg_content):
                    # This is a duplicate, don't add it
                    should_add = False
                    break
                    
        if should_add:
            self.conversations[chat_id].append(message)
        
    def add_messages(self, chat_id: str, messages: List[Dict[str, Any]]):
        """
        Add multiple messages to the tracked conversation, preventing duplicates.
        Each message is checked individually.
        """
        if not messages:
            return
            
        # Add each message individually to allow duplicate checking
        for message in messages:
            self.add_message(chat_id, message)
        
    def get_messages(self, chat_id: str) -> List[Dict[str, Any]]:
        """Get all tracked messages for a chat"""
        return self.conversations.get(chat_id, [])
        
    def has_messages(self, chat_id: str) -> bool:
        """Check if we have any tracked messages for this chat"""
        return chat_id in self.conversations and len(self.conversations[chat_id]) > 0

class LLMAgentClient:
    """
    A client for interacting with the LLM Agent SDK.

    Args:
        endpoint (str): The base URL of the SDK endpoint (e.g., "https://fusion-workspace.jumpad.ai").
        api_key (str): Your SDK key (x-api-key).
        agent_id (str, optional): The ID of the agent to interact with. If provided, all interactions
                                 will be with this agent by default.

    Raises:
        ValueError: If endpoint or api_key is empty.
    """
    def __init__(self, endpoint: str, api_key: str, agent_id: Optional[str] = None):
        if not endpoint:
            raise ValueError("SDK endpoint cannot be empty.")
        if not api_key:
            raise ValueError("SDK key cannot be empty.")

        # Ensure endpoint doesn't end with a slash for consistency
        self.base_url = endpoint.rstrip('/')
        self.api_key = api_key
        self.agent_id = agent_id
        self._session = requests.Session() # Use a session for potential connection pooling
        self._session.headers.update({
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        })
        
        # Initialize the conversation tracker
        self.conversation_tracker = ConversationTracker()
        
        # Store the current chat context
        self._current_chat_id = None
        self._last_response = None

    def _make_request(self, method: str, path: str, data: Optional[Dict] = None) -> Any:
        """
        Internal helper method to make SDK requests and handle responses/errors.

        Args:
            method (str): HTTP method (e.g., "GET", "POST").
            path (str): SDK path relative to the base URL (e.g., "/api/chats").
            data (Optional[Dict]): JSON payload for POST/PUT requests.

        Returns:
            Any: The parsed JSON response from the SDK.

        Raises:
            LLMAgentError: If the SDK returns an error status code or if a network error occurs.
        """
        url = f"{self.base_url}{path}"
        try:
            response = self._session.request(method, url, json=data, timeout=30) # Added timeout
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            # Handle cases where success response might have no content (e.g., 204 No Content)
            if response.status_code == 204:
                 return None
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            error_message = str(http_err)
            response_body = None
            try:
                # Attempt to get more details from the response body
                response_body = http_err.response.json()
                # Adapt based on your SDK's specific error structure
                if isinstance(response_body, dict):
                     error_detail = response_body.get('error', response_body.get('message', response_body.get('detail')))
                     if error_detail:
                         error_message = str(error_detail)
            except json.JSONDecodeError:
                # If response is not JSON or empty, use the response text
                 error_message = http_err.response.text or error_message

            raise LLMAgentError(
                status_code=http_err.response.status_code,
                error_message=error_message,
                response_body=response_body
            ) from http_err
        except requests.exceptions.RequestException as req_err:
            # Catch connection errors, timeouts, etc.
            raise LLMAgentError(status_code=503, error_message=f"Request failed: {req_err}") from req_err # Use appropriate status code

    def start_chat(self, agent_id: Optional[str] = None, initial_message: str = None) -> Dict[str, Any]:
        """
        Starts a new chat session with a specific agent.

        Args:
            agent_id (Optional[str]): The ID of the target agent. If not provided, uses the agent_id
                                     specified during client initialization.
            initial_message (str): The first message to initiate the chat.

        Returns:
            Dict[str, Any]: The parsed JSON response from the SDK, which includes
                           the new chat details and the initial messages. The chat ID
                           is expected under response['chat']['id'].

        Raises:
            ValueError: If agent_id is not provided and was not set during initialization,
                       or if initial_message is empty.
            LLMAgentError: If the SDK request fails or the response format is unexpected.
        """
        # Use agent_id from initialization if not provided
        agent_id = agent_id or self.agent_id
        
        if not agent_id:
            raise ValueError("Agent ID must be provided either during initialization or in this call.")
        if not initial_message:
            raise ValueError("Initial message cannot be empty.")

        path = "/api/chats"
        payload = {
            "message": initial_message,
            "agent_id": agent_id,
        }
        response = self._make_request("POST", path, data=payload)

        # Validate the expected response structure needed to proceed
        if not isinstance(response, dict) or 'chat' not in response or not isinstance(response['chat'], dict) or 'id' not in response['chat']:
            raise LLMAgentError(status_code=200, error_message="SDK response missing expected 'chat' object or 'chat.id' field.", response_body=response)

        # Get the chat ID
        chat_id = response['chat']['id']
        
        # Store the current chat context
        self._current_chat_id = chat_id
        self._last_response = response
        
        # Check if the response contains messages
        response_messages = response.get('messages', [])
        
        # Find any user messages in the response (to avoid duplicating)
        user_message_found = False
        for msg in response_messages:
            if (msg.get('message_type') == 'user' and 
                msg.get('message') == initial_message):
                user_message_found = True
                break
                
        # Add messages from the response
        if response_messages:
            self.conversation_tracker.add_messages(chat_id, response_messages)
            
        # If the user message wasn't in the response, create and add it
        if not user_message_found:
            user_message = {
                "id": f"local-user-{int(time.time())}",  # Generate a local ID
                "message_type": "user",
                "message": initial_message,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%S.0Z")
            }
            self.conversation_tracker.add_message(chat_id, user_message)
            
        return response  # Return the dictionary containing 'chat' and 'messages'

    def get_chat_id_from_response(self, response: Dict[str, Any]) -> str:
        """
        Helper method to safely extract the chat ID from an SDK response.

        Args:
            response (Dict[str, Any]): The SDK response containing chat data.

        Returns:
            str: The extracted chat ID.

        Raises:
            ValueError: If the chat ID cannot be found in the response.
        """
        chat_id = response.get('chat', {}).get('id')
        if not chat_id:
            raise ValueError("Could not extract chat_id from the response.")
        return chat_id
    
    def get_agent_response_from_chat(self, response: Dict[str, Any]) -> str:
        """
        Helper method to extract the agent's response message from an SDK response.

        Args:
            response (Dict[str, Any]): The SDK response containing messages data.

        Returns:
            str: The agent's response message.

        Raises:
            ValueError: If no agent message is found in the response.
        """
        messages = response.get('messages', [])
        agent_messages = [msg.get('message') for msg in messages 
                        if msg.get('message_type') == 'agent' and msg.get('message')]
        
        if not agent_messages:
            raise ValueError("No agent response message found in the SDK response.")
        
        # Return the most recent agent message (typically the first or last one in the list
        # depending on how the SDK sorts them)
        return agent_messages[0]  # Adjust index if needed based on sorting

    def get_all_agent_messages_from_chat(self, response: Dict[str, Any]) -> List[str]:
        """
        Helper method to extract all agent response messages from an SDK response.

        Args:
            response (Dict[str, Any]): The SDK response containing messages data.

        Returns:
            List[str]: A list of all agent response messages.

        Raises:
            ValueError: If no agent messages are found in the response.
        """
        messages = response.get('messages', [])
        agent_messages = [msg.get('message') for msg in messages 
                        if msg.get('message_type') == 'agent' and msg.get('message')]
        
        if not agent_messages:
            raise ValueError("No agent response messages found in the SDK response.")
        
        return agent_messages

    def get_raw_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Helper method to get the entire raw SDK response.
        This is useful when you need access to all response data beyond extracted fields.

        Args:
            response (Dict[str, Any]): The SDK response.

        Returns:
            Dict[str, Any]: The complete SDK response as-is.
        """
        return response

    def send_message(self, chat_id: Optional[str] = None, message: str = None) -> Dict[str, Any]:
        """
        Sends a message to an existing chat.

        Args:
            chat_id (Optional[str]): The ID of the target chat. If not provided, uses the current chat ID.
            message (str): The message to send.

        Returns:
            Dict[str, Any]: The parsed JSON response from the SDK.

        Raises:
            ValueError: If chat_id is not provided and no current chat exists, or if message is empty.
            LLMAgentError: If the SDK request fails.
        """
        # Use current chat_id if none provided
        chat_id = chat_id or self._current_chat_id
        
        if not chat_id:
            raise ValueError("Chat ID must be provided or an active chat must exist.")
        if not message:
            raise ValueError("Message cannot be empty.")

        path = f"/api/chats/{chat_id}/messages"
        payload = {
            "message": message,
        }
        response = self._make_request("POST", path, data=payload)
        
        # Store the current chat context if not already set
        if not self._current_chat_id:
            self._current_chat_id = chat_id
        
        self._last_response = response

        # Check if the response contains expected data
        if not isinstance(response, dict):
            raise LLMAgentError(status_code=200, error_message="SDK response format is unexpected.", response_body=response)

        # Handle message tracking
        sent_message = None
        for msg in response.get('messages', []):
            if msg.get('message_type') == 'user' and msg.get('message') == message:
                sent_message = msg
                break
            
        # If no user message found in response, create one locally
        if not sent_message:
            sent_message = {
                "id": f"local-user-{int(time.time())}",  # Generate a local ID
                "message_type": "user",
                "message": message,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%S.0Z")
            }
        
        # Add all messages to our tracker, including the sent one if needed
        response_messages = response.get('messages', [])
        if response_messages:
            self.conversation_tracker.add_messages(chat_id, response_messages)
        else:
            # If no messages in response, at least add our sent message
            self.conversation_tracker.add_message(chat_id, sent_message)
            
        return response
        
    def get_sent_message_content(self, response: Dict[str, Any]) -> str:
        """
        Helper method to extract the message content from a send_message response.
        
        Args:
            response (Dict[str, Any]): The response from send_message SDK call.
            
        Returns:
            str: The message content.
            
        Raises:
            ValueError: If the message content cannot be found in the response.
        """
        # The response contains an array of messages
        messages = response.get('messages', [])
        if not messages:
            raise ValueError("No messages found in the send_message response.")
            
        # Find the user message (our sent message)
        for msg in messages:
            if msg.get('message_type') == 'user' and msg.get('message'):
                return msg.get('message')
                
        raise ValueError("Could not find user message content in the send_message response.")
        
    def get_sent_message_id(self, response: Dict[str, Any]) -> str:
        """
        Helper method to extract the message ID from a send_message response.
        
        Args:
            response (Dict[str, Any]): The response from send_message SDK call.
            
        Returns:
            str: The message ID.
            
        Raises:
            ValueError: If the message ID cannot be found in the response.
        """
        # The response contains an array of messages
        messages = response.get('messages', [])
        if not messages:
            raise ValueError("No messages found in the send_message response.")
            
        # Find the user message (our sent message)
        for msg in messages:
            if msg.get('message_type') == 'user' and msg.get('id'):
                return msg.get('id')
                
        raise ValueError("Could not find user message ID in the send_message response.")
        
    def get_agent_reply_to_message(self, response: Dict[str, Any]) -> str:
        """
        Helper method to extract the agent's reply to our sent message.
        
        Args:
            response (Dict[str, Any]): The response from send_message SDK call.
            
        Returns:
            str: The agent's reply message.
            
        Raises:
            ValueError: If the agent reply cannot be found in the response.
        """
        # The response contains an array of messages
        messages = response.get('messages', [])
        if not messages:
            raise ValueError("No messages found in the send_message response.")
            
        # Find the agent message (the reply to our message)
        for msg in messages:
            if msg.get('message_type') == 'agent' and msg.get('message'):
                return msg.get('message')
                
        raise ValueError("Could not find agent reply in the send_message response.")

    def get_chat_history(self, chat_id: str) -> Dict[str, Any]:
        """
        Retrieves the chat details without message history, as the SDK doesn't support message history retrieval.
        Messages are tracked internally by the client instead.

        Args:
            chat_id (str): The ID of the chat to retrieve.

        Returns:
            Dict[str, Any]: The parsed JSON response containing the chat details.

        Raises:
            ValueError: If chat_id is empty.
            LLMAgentError: If the SDK request fails.
        """
        if not chat_id:
            raise ValueError("Chat ID cannot be empty.")

        # Get chat details
        chat_path = f"/api/chats/{chat_id}"
        chat_details = self._make_request("GET", chat_path)
        
        return chat_details
    
    def get_chat_with_messages(self, chat_id: str) -> Dict[str, Any]:
        """
        Retrieves a chat with its complete message history using our message tracker.
        Since the SDK doesn't provide a way to get message history, we use our locally tracked messages.
        Duplicate messages are automatically handled by the conversation tracker.
        
        Args:
            chat_id (str): The ID of the chat to retrieve.

        Returns:
            Dict[str, Any]: The chat object with messages included from our tracker.

        Raises:
            ValueError: If chat_id is empty.
            LLMAgentError: If the SDK request fails.
        """
        if not chat_id:
            raise ValueError("Chat ID cannot be empty.")

        # First get the chat details
        chat_path = f"/api/chats/{chat_id}"
        chat_details = self._make_request("GET", chat_path)
        
        # Get messages from our conversation tracker
        tracked_messages = self.conversation_tracker.get_messages(chat_id)
        if isinstance(chat_details, dict):
            chat_details['messages'] = tracked_messages
            
        return chat_details
        
    def get_tracked_messages(self, chat_id: str, format_output: bool = False) -> List[Dict[str, Any]]:
        """
        Get all messages tracked in memory for a specific chat.
        This is the main method to get message history as the SDK doesn't provide this functionality.
        
        Args:
            chat_id (str): The ID of the chat to retrieve messages for.
            format_output (bool, optional): Whether to return a nicely formatted string output instead of raw messages. Defaults to False.
            
        Returns:
            If format_output is False:
                List[Dict[str, Any]]: A list of all tracked messages for this chat.
            If format_output is True:
                str: A nicely formatted string containing the complete conversation.
        """
        messages = self.conversation_tracker.get_messages(chat_id)
        
        if format_output:
            if not messages:
                return "No messages found in this conversation."
                
            # Sort messages by timestamp to ensure chronological order
            sorted_messages = sorted(
                messages,
                key=lambda x: x.get('created_at', '') # Sort by timestamp
            )
            
            # Format as a readable string
            output = "===== Conversation History =====\n\n"
            for i, msg in enumerate(sorted_messages, 1):
                msg_type = msg.get('message_type')
                content = msg.get('message')
                
                if msg_type and content:
                    if msg_type == 'user':
                        prefix = "👤 You: "
                    else:
                        prefix = "🤖 Agent: "
                    
                    output += f"{i}. {prefix}{content}\n\n"
            
            return output
        
        return messages
        
    def get_tracked_user_messages(self, chat_id: str, format_output: bool = False) -> Union[List[Dict[str, Any]], str]:
        """
        Get all user messages tracked for a specific chat.
        
        Args:
            chat_id (str): The ID of the chat to retrieve messages for.
            format_output (bool, optional): Whether to return a nicely formatted string output. Defaults to False.
            
        Returns:
            If format_output is False:
                List[Dict[str, Any]]: A list of all user messages for this chat.
            If format_output is True:
                str: A nicely formatted string containing all user messages.
            
        Raises:
            ValueError: If no user messages are found.
        """
        messages = self.get_tracked_messages(chat_id)
        user_messages = [msg for msg in messages if msg.get('message_type') == 'user']
        
        if not user_messages:
            raise ValueError("No user messages found in the tracked conversation.")
            
        if format_output:
            # Sort messages by timestamp
            sorted_messages = sorted(
                user_messages,
                key=lambda x: x.get('created_at', '') # Sort by timestamp
            )
            
            # Format as a readable string
            output = "===== Your Messages =====\n\n"
            for i, msg in enumerate(sorted_messages, 1):
                content = msg.get('message')
                output += f"{i}. {content}\n\n"
                
            return output
            
        return user_messages
        
    def get_tracked_agent_messages(self, chat_id: str, format_output: bool = False) -> Union[List[Dict[str, Any]], str]:
        """
        Get all agent messages tracked for a specific chat.
        
        Args:
            chat_id (str): The ID of the chat to retrieve messages for.
            format_output (bool, optional): Whether to return a nicely formatted string output. Defaults to False.
            
        Returns:
            If format_output is False:
                List[Dict[str, Any]]: A list of all agent messages for this chat.
            If format_output is True:
                str: A nicely formatted string containing all agent messages.
            
        Raises:
            ValueError: If no agent messages are found.
        """
        messages = self.get_tracked_messages(chat_id)
        agent_messages = [msg for msg in messages if msg.get('message_type') == 'agent']
        
        if not agent_messages:
            raise ValueError("No agent messages found in the tracked conversation.")
            
        if format_output:
            # Sort messages by timestamp
            sorted_messages = sorted(
                agent_messages,
                key=lambda x: x.get('created_at', '') # Sort by timestamp
            )
            
            # Format as a readable string
            output = "===== Agent Responses =====\n\n"
            for i, msg in enumerate(sorted_messages, 1):
                content = msg.get('message')
                output += f"{i}. {content}\n\n"
                
            return output
            
        return agent_messages

    def get_chat_id(self) -> str:
        """
        Get the current chat ID without needing to provide any parameters.
        
        Returns:
            str: The current chat ID.
            
        Raises:
            ValueError: If no chat has been started yet.
        """
        if not self._current_chat_id:
            raise ValueError("No active chat session. Call start_chat() or send_message() first.")
        return self._current_chat_id
        
    def get_agent_response(self, message: Optional[str] = None) -> str:
        """
        Get a response from the agent, automatically handling whether this is the first message
        (requiring start_chat) or a follow-up message (requiring send_message).
        
        This method simplifies the developer experience by providing a single method to 
        communicate with the agent regardless of message sequence.
        
        Args:
            message (Optional[str]): The message to send to the agent. If None, and a previous
                                    response exists, will extract the agent's response from that.
                                    
        Returns:
            str: The agent's response.
            
        Raises:
            ValueError: If no message is provided for a new chat, or if a required agent_id
                       was not provided during initialization.
        """
        # If no chat has been started and a message is provided, start a new chat
        if not self._current_chat_id and message:
            if not self.agent_id:
                raise ValueError("No agent_id provided. Initialize the client with an agent_id or call start_chat with agent_id.")
            response = self.start_chat(initial_message=message)
            return self.get_agent_response_from_chat(response)
            
        # If a chat exists and a message is provided, send the message
        elif self._current_chat_id and message:
            response = self.send_message(chat_id=self._current_chat_id, message=message)
            self._last_response = response
            try:
                return self.get_agent_reply_to_message(response)
            except ValueError:
                # If no immediate reply, return a placeholder
                return "Agent is processing your message..."
                
        # If no message but we have a previous response, extract agent message from it
        elif self._last_response:
            try:
                return self.get_agent_response_from_chat(self._last_response)
            except ValueError:
                try:
                    return self.get_agent_reply_to_message(self._last_response)
                except ValueError:
                    # Try to get the most recent agent message from the conversation
                    try:
                        agent_messages = self.get_tracked_agent_messages(self._current_chat_id)
                        if agent_messages:
                            return agent_messages[0].get('message', "No agent response found.")
                    except ValueError:
                        pass
                    return "No agent response found in the current context."
        else:
            raise ValueError("No message provided and no previous response to extract from.")
            
    def get_raw_agent_response(self) -> Dict[str, Any]:
        """
        Get the raw response data from the last agent interaction.
        
        Returns:
            Dict[str, Any]: The raw response data.
            
        Raises:
            ValueError: If no response exists yet.
        """
        if not self._last_response:
            raise ValueError("No agent response available yet.")
        return self._last_response 