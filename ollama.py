# qwen2.5:72b 

import requests
from typing import Any, Dict, Optional
import json

class OllamaClient:
    def __init__(
        self,
        endpoint: str = "http://localhost:11434",
        api_key: Optional[str] = None,
        timeout: int = 60,
        headers: Optional[Dict[str, str]] = None,
        chat_system_prompt: str = "tell me a quick story"
    ):
        """
        Initialize the OllamaClient.

        :param endpoint: The base URL of the Ollama instance.
        :param api_key: An optional API key for authentication.
        :param timeout: Timeout in seconds for requests.
        :param headers: Additional HTTP headers to include in requests.
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.timeout = timeout
        self.headers = headers or {}
        self.chat_history = [{"role": "system", "content": chat_system_prompt}]
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def _request(self, method: str, path: str, **kwargs) -> Any:
        """
        Make a request to the Ollama API.

        :param method: HTTP method (GET, POST, etc.).
        :param path: The API endpoint path.
        :param kwargs: Additional arguments for requests.request().
        :return: JSON response from the server.
        """
        url = f"{self.endpoint}{path}"
        response = requests.request(method, url, headers=self.headers, timeout=self.timeout, **kwargs)
        
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
        return response.json()
    
    def chat(self, prompt: str, model: Optional[str] = None, stream: Optional[bool] = False) -> Dict[str, Any]:
        """
        Chat with the Ollama instance.

        :param prompt: The input prompt for the model.
        :param model: The name of the model to use. If not specified, the default model is used.
        :return: JSON response containing the generated text.
        """
        payload = {"stream": stream}
        if model:
            payload["model"] = model
        self.chat_history.append({"role": "user", "content": prompt})
        payload["messages"] = self.chat_history
        response = self._request("POST", "/api/chat", json=payload)
        self.chat_history.append(response['message'])
        return response['message']['content']
    
    def chat_reset(self):
        """
        Reset the chat history.
        """
        self.chat_history = self.chat_history[0:1]

    def generate(self, prompt: str, model: Optional[str] = None, stream: Optional[bool] = False) -> Dict[str, Any]:
        """
        Generate a response from the Ollama instance.

        :param prompt: The input prompt for the model.
        :param model: The name of the model to use. If not specified, the default model is used.
        :return: JSON response containing the generated text.
        """
        payload = {"prompt": prompt}
        payload["stream"] = stream
        if model:
            payload["model"] = model

        return self._request("POST", "/api/generate", json=payload)

    def list_models(self) -> Dict[str, Any]:
        """
        List all available models on the Ollama instance.

        :return: JSON response containing a list of models.
        """
        return self._request("GET", "/api/tags")

# Example usage
if __name__ == "__main__":
    client = OllamaClient(
        endpoint="http://192.168.1.182:11434",
        timeout=90,

    )

    try:
        # Generate a response
        prompt = "tell me a quick story"
        response = client.generate(prompt, model="llama3.3:latest", )
        print("Generated Response:", response["response"])
    
    except Exception as e:
        print(f"An error occurred: {e}")