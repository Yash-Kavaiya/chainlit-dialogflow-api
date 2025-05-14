from google.cloud.dialogflowcx_v3beta1.services.agents import AgentsClient
from google.cloud.dialogflowcx_v3beta1.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3beta1.types import session
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DialogflowHandler:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location_id = os.getenv("DIALOGFLOW_LOCATION", "global")
        self.agent_id = os.getenv("DIALOGFLOW_AGENT_ID")
        self.agent = f"projects/{self.project_id}/locations/{self.location_id}/agents/{self.agent_id}"
        self.language_code = "en"
        
        # Create a unique session ID for each instance
        self.session_id = str(uuid.uuid4())
        
        # Initialize client options
        self.client_options = None
        
        # Set API endpoint for non-global locations
        if self.location_id != "global":
            api_endpoint = f"{self.location_id}-dialogflow.googleapis.com:443"
            self.client_options = {"api_endpoint": api_endpoint}
            
        # Initialize session client
        self.session_client = SessionsClient(client_options=self.client_options)
        
    def get_session_path(self):
        """Get the session path."""
        return f"{self.agent}/sessions/{self.session_id}"
    
    def detect_intent(self, text):
        """Detects intent from user text input.
        
        Args:
            text (str): The user's input text
            
        Returns:
            list: A list of response messages from Dialogflow
        """
        session_path = self.get_session_path()
        text_input = session.TextInput(text=text)
        query_input = session.QueryInput(text=text_input, language_code=self.language_code)
        
        request = session.DetectIntentRequest(
            session=session_path, query_input=query_input
        )
        
        response = self.session_client.detect_intent(request=request)
        
        # Extract response messages
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages
        ]
        
        return response_messages