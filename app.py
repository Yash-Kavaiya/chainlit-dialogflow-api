import os
import chainlit as cl
from dialogflow_handler import DialogflowHandler
from dotenv import load_dotenv

# Make sure to load environment variables before Chainlit imports
load_dotenv()

# Check if the JWT secret is set
if not os.getenv("CHAINLIT_AUTH_SECRET"):
    # Generate a temporary one if not found
    import secrets
    os.environ["CHAINLIT_AUTH_SECRET"] = secrets.token_hex(16)
    print("WARNING: Using a temporary CHAINLIT_AUTH_SECRET. For production, set this in your .env file.")

# Initialize DialogflowHandler
dialogflow = None

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session"""
    global dialogflow
    
    # Initialize Dialogflow handler
    dialogflow = DialogflowHandler()
    
    # Send welcome message
    await cl.Message(
        content="👋 Hello! I'm your Dialogflow CX assistant. How can I help you today?",
        author="Assistant"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle user messages"""
    # Show typing indicator
    async with cl.Step(name="Thinking..."):
        # Get response from Dialogflow
        responses = dialogflow.detect_intent(message.content)
        
        # Join multiple responses if any
        response_text = " ".join(responses)
    
    # Send the final response
    await cl.Message(
        content=response_text,
        author="Assistant"
    ).send()

if __name__ == "__main__":
    # Chainlit is launched via the CLI command:
    # chainlit run app.py
    pass