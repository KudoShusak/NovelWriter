import requests
import json
from config import Config

class LLMClient:
    def __init__(self, model_name=None, base_url=None):
        self.model = model_name or Config.DEFAULT_MODEL
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        self.api_generate = f"{self.base_url}/api/generate"

    def generate_text(self, prompt, system_prompt=None, temperature=0.7):
        """
        Generates text using Ollama API.
        """
        full_prompt = prompt
        if system_prompt:
            # Some models behave better with system prompts integrated differently,
            # but for standard Ollama usage, we can pass 'system' parameter if supported
            # or prepend it. Here we will use the 'system' parameter in the payload.
            pass

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(self.api_generate, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            return ""

if __name__ == "__main__":
    # Test
    client = LLMClient()
    print(client.generate_text("Hello, are you ready to write a novel?", system_prompt="You are a helpful assistant."))
