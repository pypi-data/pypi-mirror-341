# Jumpad SDK Client

A powerful and user-friendly Python client for interacting with the Jumpad AI Agent SDK.

[![PyPI version](https://badge.fury.io/py/jumpad-sdk-client.svg)](https://pypi.org/project/jumpad-sdk-client/)
[![GitHub](https://img.shields.io/github/license/jumpad-ai/jumpad-python-sdk)](https://github.com/jumpad-ai/jumpad-python-sdk/blob/main/LICENSE)

## Features

- Easy-to-use SDK with simplified API that abstracts away complexity
- Automatic handling of chat sessions and message sequences
- Two supported approaches: simplified for ease of use, traditional for detailed control
- Automatic tracking of conversation history
- Duplicate message prevention
- Helper methods for extracting different types of messages
- Pretty-formatted conversation output

## Installation

Make sure you have the latest version of pip before installing:

```bash
pip install --upgrade pip
```

Install from PyPI:

```bash
pip install jumpad-sdk-client
```

## Quick Start

```python
from jumpad_sdk_client import LLMAgentClient

# Initialize the client with your API key and Agent ID
BASE_URL = "your_fusion_workspace_instance_URL"
API_KEY = "your_api_key_here"
AGENT_ID = "your_agent_id_here"

client = LLMAgentClient(endpoint=BASE_URL, api_key=API_KEY, agent_id=AGENT_ID)

# Simply send a message and get a response - the SDK handles everything
agent_response = client.get_agent_response("Hi Agent, can you introduce yourself?")
print(f"Agent says: {agent_response}")

# Send a follow-up message - no need to manage chat IDs
follow_up_response = client.get_agent_response("Thanks! Now tell me a fun fact.")
print(f"Agent's reply: {follow_up_response}")

# If you need the chat ID for any reason, you can get it anytime
chat_id = client.get_chat_id()
print(f"Chat ID: {chat_id}")

# If you need the raw response data
raw_response = client.get_raw_agent_response()
print(f"Raw response: {raw_response}")
```

## Working with Conversations

### Viewing the Complete Conversation

```python
# Get nicely formatted conversation history
formatted_history = client.get_tracked_messages(chat_id, format_output=True)
print(formatted_history)

# Output example:
# ===== Conversation History =====
#
# 1. 👤 You: Hi Agent, can you introduce yourself?
#
# 2. 🤖 Agent: Hello! I'm the Jumpad AI assistant...
#
# 3. 👤 You: Thanks! Now tell me a fun fact.
#
# 4. 🤖 Agent: Here's a fun fact: Honey never spoils...
```

### Working with User Messages

```python
# Get all user messages in formatted output
try:
    user_messages = client.get_tracked_user_messages(chat_id, format_output=True)
    print(user_messages)
except ValueError as e:
    print(f"Error: {e}")

# Get raw user message data for processing
try:
    user_messages_data = client.get_tracked_user_messages(chat_id)
    for msg in user_messages_data:
        print(f"ID: {msg.get('id')}, Message: {msg.get('message')}")
except ValueError as e:
    print(f"Error: {e}")
```

### Working with Agent Messages

```python
# Get all agent responses in formatted output
try:
    agent_messages = client.get_tracked_agent_messages(chat_id, format_output=True)
    print(agent_messages)
except ValueError as e:
    print(f"Error: {e}")

# Get raw agent message data for processing
try:
    agent_messages_data = client.get_tracked_agent_messages(chat_id)
    for msg in agent_messages_data:
        print(f"ID: {msg.get('id')}, Message: {msg.get('message')}")
except ValueError as e:
    print(f"Error: {e}")
```

## Advanced Usage

### Traditional API Usage (Still Supported)

If you prefer the previous style of explicit chat management:

```python
# Start a chat session explicitly
response = client.start_chat(initial_message="Hello agent!")

# Extract the chat ID
chat_id = client.get_chat_id_from_response(response)

# Get the agent's response
agent_response = client.get_agent_response_from_chat(response)

# Send a follow-up message to the specific chat
send_response = client.send_message(chat_id=chat_id, message="Follow up question")

# Get the agent's reply
agent_reply = client.get_agent_reply_to_message(send_response)
```

### Getting Chat Details

```python
# Get chat metadata without messages
chat_details = client.get_chat_history(chat_id)
print(f"Chat title: {chat_details.get('title')}")
print(f"Chat created at: {chat_details.get('created_at')}")

# Get chat with messages
chat_with_messages = client.get_chat_with_messages(chat_id)
```

### Extracting Message Details

```python
# After sending a message either with the simplified or traditional API
# you can extract specific details if needed

# Extract the sent message content
message_content = client.get_sent_message_content(client.get_raw_agent_response())

# Extract the sent message ID
message_id = client.get_sent_message_id(client.get_raw_agent_response())
```

### Getting Raw SDK Responses

```python
# Get the raw SDK response
raw_response = client.get_raw_response(response)
print(json.dumps(raw_response, indent=2))
```

## Error Handling

The client includes comprehensive error handling:

```python
from jumpad_sdk_client import LLMAgentClient, LLMAgentError

try:
    # Your code here
    response = client.send_message(chat_id, "Hello")
except LLMAgentError as e:
    print(f"SDK Error: {e.status_code} - {e.error_message}")
    if e.response_body:
        print(f"Response Body: {e.response_body}")
except ValueError as e:
    print(f"Value Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

## Getting Help

You can use Python's built-in help system to learn more about the package:

```python
import jumpad_sdk_client
help(jumpad_sdk_client)  # Show module documentation

from jumpad_sdk_client import LLMAgentClient
help(LLMAgentClient)  # Show class documentation 
help(LLMAgentClient.send_message)  # Show method documentation
```

## Complete Example

```python
import os
import json
from jumpad_sdk_client import LLMAgentClient, LLMAgentError

# Configuration
BASE_URL = "https://fusion-workspace.jumpad.ai"
API_KEY = "your_api_key_here"  # Replace with your actual API key
AGENT_ID = "your_agent_id_here"  # Replace with your actual agent ID

def main():
    try:
        # Initialize the client with your agent ID
        client = LLMAgentClient(endpoint=BASE_URL, api_key=API_KEY, agent_id=AGENT_ID)
        print("Client initialized.")

        # Send the first message and get the agent's response
        agent_response = client.get_agent_response("Hi Agent, can you introduce yourself?")
        print(f"Agent says: {agent_response}")
        
        # Send a follow-up message
        follow_up_response = client.get_agent_response("Thanks! Tell me about your capabilities.")
        print(f"Agent reply: {follow_up_response}")
        
        # Get the chat ID if needed for reference
        chat_id = client.get_chat_id()
        print(f"Conversation is happening in chat: {chat_id}")
        
        # Display the complete conversation
        print("\nComplete conversation:")
        conversation = client.get_tracked_messages(chat_id, format_output=True)
        print(conversation)
        
    except LLMAgentError as e:
        print(f"SDK Error: {e.status_code} - {e.error_message}")
        if e.response_body:
            print(f"Response: {json.dumps(e.response_body, indent=2)}")
    except ValueError as e:
        print(f"Value Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()
```

## SDK Reference

### LLMAgentClient

- `__init__(endpoint: str, api_key: str, agent_id: Optional[str] = None)` - Initialize the client with optional agent_id
- `start_chat(agent_id: Optional[str] = None, initial_message: str)` - Start a new chat
- `send_message(chat_id: Optional[str] = None, message: str)` - Send a message to a chat

### Simplified API Methods

- `get_agent_response(message: Optional[str] = None)` - Get agent's response (handles chat initiation automatically)
- `get_chat_id()` - Get current chat ID without needing parameters
- `get_raw_agent_response()` - Get raw response data from last interaction

### Traditional Helper Methods

- `get_chat_id_from_response(response)` - Extract chat ID from response
- `get_agent_response_from_chat(response)` - Extract agent response
- `get_sent_message_content(response)` - Get content of sent message
- `get_sent_message_id(response)` - Get ID of sent message 
- `get_agent_reply_to_message(response)` - Get agent's reply to a message

### Message Tracking

- `get_tracked_messages(chat_id, format_output=False)` - Get all messages
- `get_tracked_user_messages(chat_id, format_output=False)` - Get user messages
- `get_tracked_agent_messages(chat_id, format_output=False)` - Get agent messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.