from openai import OpenAI


class DeepSeekAgent:

    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.context = {
            "role": "system",
            "content": "You are an AI assistant specialized in football. You are able to answer questions about football and provide information about upcoming games, teams, and players.",
        }

    def list_models(self) -> list:
        """List available models from DeepSeek API."""
        response = self.client.models.list()
        return response

    def process_input(self, user_input: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[self.context, {"role": "user", "content": user_input}],
        )
        return response.choices[0].message.content
