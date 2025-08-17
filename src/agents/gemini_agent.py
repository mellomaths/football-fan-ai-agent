from google import genai


class GeminiAgent:

    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.client = genai.Client(
            api_key=api_key,
        )

    def list_models(self):
        """List available models from Gemini API."""
        return self.client.models.list()

    def process_user_input(self, user_input: str) -> str:
        """Process user input and return the model's response."""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=user_input,
        )
        return response.text if response.text else "No response from model."
