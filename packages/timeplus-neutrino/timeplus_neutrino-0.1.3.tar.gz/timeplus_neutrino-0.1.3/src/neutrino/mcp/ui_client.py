# app.py
import asyncio
import os
from typing import Optional, Dict
from contextlib import AsyncExitStack

import uvicorn
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

app = FastAPI()

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Connection manager to handle WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)


class MCPClient:
    def __init__(self, server_script_path: str):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 1000
        self.server_script_path = server_script_path
        self.is_connected = False

    async def connect_to_server(self):
        """Connect to an MCP server"""
        if self.is_connected:
            return

        server_script_path = self.server_script_path
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        self.is_connected = True
        return [tool.name for tool in tools]

    async def get_available_tools(self):
        """Get list of available tools in the format required by Claude API"""
        if not self.is_connected:
            await self.connect_to_server()

        response = await self.session.list_tools()
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

    async def process_query(
        self, query: str, websocket_manager=None, client_id=None
    ) -> str:
        """Process a query using Claude and available tools with reactive pattern support"""
        if not self.is_connected:
            await self.connect_to_server()

        # Initialize conversation with the user query
        messages = [{"role": "user", "content": query}]

        # Get available tools
        available_tools = await self.get_available_tools()

        # Track all responses for final output
        all_responses = []

        # Continue conversation until Claude has no more tool calls to make
        while True:
            # Call Claude with current conversation state
            response = self.anthropic.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=messages,
                tools=available_tools,
            )

            # Process the response
            has_tool_calls = False
            assistant_message_content = []

            for content in response.content:
                if content.type == "text":
                    # Store text response
                    all_responses.append(content.text)
                    assistant_message_content.append(content)

                    # Send text to websocket if available
                    if websocket_manager and client_id:
                        await websocket_manager.send_message(content.text, client_id)

                elif content.type == "tool_use":
                    # Found a tool call
                    has_tool_calls = True
                    tool_name = content.name
                    tool_args = content.input

                    # Log the tool call
                    tool_call_msg = f"[Calling tool {tool_name} with args {tool_args}]"
                    all_responses.append(tool_call_msg)

                    # Send tool call notification to websocket if available
                    if websocket_manager and client_id:
                        await websocket_manager.send_message(tool_call_msg, client_id)

                    # Execute the tool call
                    result = await self.session.call_tool(tool_name, tool_args)

                    # Append the assistant's message with the tool call
                    assistant_message_content.append(content)

                    # Update messages with this assistant response
                    messages.append(
                        {"role": "assistant", "content": assistant_message_content}
                    )

                    # Add tool result as user message
                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": content.id,
                                    "content": result.content,
                                }
                            ],
                        }
                    )

                    # We've handled this tool call, break to process next Claude response
                    break

            # If no tool calls were made, add assistant's message and exit the loop
            if not has_tool_calls:
                # If there's any remaining text content to add, add it to messages
                if assistant_message_content:
                    messages.append(
                        {"role": "assistant", "content": assistant_message_content}
                    )
                break

            # Loop continues if there were tool calls, allowing Claude to make multiple calls

        return "\n".join(all_responses)

    async def cleanup(self):
        """Clean up resources"""
        if self.is_connected:
            await self.exit_stack.aclose()
            self.is_connected = False


# Message data models
class Message(BaseModel):
    query: str


# Global MCP client instance
mcp_client = None
manager = ConnectionManager()


# Setup routes
@app.on_event("startup")
async def startup_event():
    global mcp_client
    # You'll need to set this to your server script path
    server_script_path = os.getenv("MCP_SERVER_SCRIPT", "server.py")
    mcp_client = MCPClient(server_script_path)
    await mcp_client.connect_to_server()
    print(
        f"Connected to MCP server with tools: {await mcp_client.get_available_tools()}"
    )


@app.on_event("shutdown")
async def shutdown_event():
    global mcp_client
    if mcp_client:
        await mcp_client.cleanup()


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/query")
async def process_query(message: Message):
    global mcp_client
    if not mcp_client:
        raise HTTPException(status_code=500, detail="MCP client not initialized")

    response = await mcp_client.process_query(message.query)
    return {"response": response}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    global mcp_client, manager

    if not mcp_client:
        await websocket.close(code=1011, reason="MCP client not initialized")
        return

    await manager.connect(websocket, client_id)

    try:
        while True:
            query = await websocket.receive_text()
            # Process in background task to not block the WebSocket
            asyncio.create_task(
                mcp_client.process_query(
                    query, websocket_manager=manager, client_id=client_id
                )
            )
    except WebSocketDisconnect:
        manager.disconnect(client_id)


# Generate HTML template file
def create_html_template():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP Chat Interface</title>
    <style>
        /* Base Layout */
        body {
            font-family: 'Inter', 'Arial', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 24px;
            background-color: #19171D; /* Dark background */
            color: #EFEEEF; /* Light text for contrast */
        }

        /* Chat Container */
        #chat-container {
            display: flex;
            flex-direction: column;
            height: 70vh;
            border: 1px solid #2F2D32;
            border-radius: 8px;
            margin-bottom: 24px;
            background-color: #242227; /* Slightly lighter than body */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        }

        /* Chat Messages */
        #chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            background-color: #242227;
        }

        /* User Input Section */
        #user-input {
            display: flex;
            border-top: 1px solid #2F2D32;
            padding: 8px;
            background-color: #242227;
        }

        /* Message Input Field */
        #message-input {
            flex: 1;
            padding: 16px;
            border: 1px solid #2F2D32;
            border-radius: 4px;
            background-color: #19171D;
            color: #F0F6FC;
            outline: none;
        }

        /* Send Button */
        #send-button {
            padding: 8px 16px;
            background-color: #B83280; /* Timeplus primary pink */
            color: #FFFFFF;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        #send-button:hover {
            background-color: #8A2660;
        }

        /* Message Bubbles */
        .message {
            margin-bottom: 16px;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 80%;
            font-size: 14px;
            line-height: 1.5;
        }

        /* User Message */
        .user-message {
            background-color: #B83280; /* Match send button color */
            color: #FFFFFF;
            align-self: flex-end;
            margin-left: auto;
        }

        /* Assistant Message */
        .assistant-message {
            background-color: #242227;
            color: #EFEEEF;
            align-self: flex-start;
        }

        /* Status Text */
        #status {
            margin-bottom: 16px;
            color: #AEACB0;
            font-size: 12px;
        }

    </style>
</head>
<body>
    <h1>AI Assistant of Timeplus</h1>
    <div id="status">Status: Disconnected</div>
    <div id="chat-container">
        <div id="chat-messages"></div>
        <div id="user-input">
            <input type="text" id="message-input" placeholder="Type your message here...">
            <button id="send-button">Send</button>
        </div>
    </div>

    <script>
        const clientId = Math.random().toString(36).substring(2, 15);
        let socket = null;
        const chatMessages = document.getElementById('chat-messages');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const statusElement = document.getElementById('status');

        function connectWebSocket() {
            socket = new WebSocket(`ws://${window.location.host}/ws/${clientId}`);

            socket.onopen = function(e) {
                statusElement.textContent = 'Status: Connected';
                statusElement.style.color = 'green';
                sendButton.disabled = false;
            };

            socket.onmessage = function(event) {
                const message = event.data;
                addMessage(message, 'assistant');
            };

            socket.onclose = function(event) {
                statusElement.textContent = 'Status: Disconnected';
                statusElement.style.color = 'red';
                sendButton.disabled = true;
                // Try to reconnect after a delay
                setTimeout(connectWebSocket, 3000);
            };

            socket.onerror = function(error) {
                statusElement.textContent = 'Status: Error - check console for details';
                statusElement.style.color = 'red';
                console.error('WebSocket error:', error);
            };
        }

        function addMessage(content, sender) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            messageElement.classList.add(sender + '-message');

            // Handle tool call messages with special formatting
            if (content.startsWith('[Calling tool')) {
                messageElement.style.color = '#0066cc';
                messageElement.style.fontStyle = 'italic';
            }

            messageElement.textContent = content;
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function sendMessage() {
            const message = messageInput.value.trim();
            if (message && socket && socket.readyState === WebSocket.OPEN) {
                socket.send(message);
                addMessage(message, 'user');
                messageInput.value = '';
            }
        }

        // Event listeners
        sendButton.addEventListener('click', sendMessage);

        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Connect when page loads
        connectWebSocket();
    </script>
</body>
</html>
"""
    os.makedirs("templates", exist_ok=True)
    with open("templates/index.html", "w") as f:
        f.write(html_content)


# Create the HTML template
create_html_template()

# Run the server
if __name__ == "__main__":
    import sys

    # Check if server script path is provided as an argument
    if len(sys.argv) > 1:
        os.environ["MCP_SERVER_SCRIPT"] = sys.argv[1]

    uvicorn.run("neutrino.mcp.ui_client:app", host="0.0.0.0", port=5001, reload=True)
