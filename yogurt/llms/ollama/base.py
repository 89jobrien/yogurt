import httpx
import json
from typing import Any, AsyncIterator, Iterator, List, Optional

from yogurt.llms.base import BaseLLM
from yogurt.output.base import Generation, LLMResult
from yogurt.prompts.prompt_value import PromptValue
from yogurt.messages.base import HumanMessage
from yogurt.types.api import APIRequest, APIResponse

class OllamaLLM(BaseLLM):
    """
    An LLM class that integrates with an Ollama service via direct API calls
    to the /api/generate endpoint. This class is best for simple, non-chat
    completions.
    """

    model_config = {
        "arbitrary_types_allowed": True,
    }

    host: str = "http://localhost:11434"

    def _build_payload(self, prompt: PromptValue, stream: bool, **kwargs: Any) -> dict:
        """
        Helper to construct the JSON payload for the Ollama /api/generate endpoint.
        Uses raw mode to prevent server-side templating.
        """
        full_prompt_str = prompt.to_string()

        payload = {
            "model": self.model_name,
            "prompt": full_prompt_str,
            "stream": stream,
            "raw": True,
            "options": {"temperature": self.temperature, **kwargs},
        }
        return payload

    def _generate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """Generates a response using the /api/generate endpoint."""
        payload = self._build_payload(prompt, stream=False, **kwargs)
        request = APIRequest(
            method="POST",
            url=f"{self.host}/api/generate",
            body=payload
        )

        print("\n--- Sending Payload to Ollama /api/generate ---")
        print(json.dumps(request.body, indent=2))
        print("---------------------------------")

        with httpx.Client() as client:
            response = client.request(
                method=request.method,
                url=request.url,
                json=request.body,
                timeout=120
            )
            response.raise_for_status()
            api_response = APIResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
                body=response.json()
            )
        data = api_response.body

        generation = Generation(
            text=data.get("response", ""),
            metadata=data,
        )
        return LLMResult(generations=[generation], llm_output=data)

    def invoke(self, input_str: str, **kwargs: Any) -> str:
        prompt = PromptValue(text=input_str)
        result = self.generate(prompt, **kwargs)
        return result.generations[0].text

    def stream(self, prompt: PromptValue, **kwargs: Any) -> Iterator[dict]:
        """Streams response chunks from the /api/generate endpoint."""
        payload = self._build_payload(prompt, stream=True, **kwargs)
        request = APIRequest(
            method="POST",
            url=f"{self.host}/api/generate",
            body=payload
        )
        with httpx.Client() as client:
            with client.stream(
                method=request.method,
                url=request.url,
                json=request.body,
                timeout=120
            ) as response:
                for chunk in response.iter_lines():
                    if chunk:
                        yield json.loads(chunk)

    async def agenerate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        payload = self._build_payload(prompt, stream=False, **kwargs)
        request = APIRequest(
            method="POST",
            url=f"{self.host}/api/generate",
            body=payload
        )
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=request.url,
                json=request.body,
                timeout=120
            )
            response.raise_for_status()
            api_response = APIResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
                body=await response.json()
            )
        data = api_response.body

        generation = Generation(
            text=data.get("response", ""),
            metadata=data,
        )
        return LLMResult(generations=[generation], llm_output=data)

    async def ainvoke(self, input_str: str, **kwargs: Any) -> str:
        prompt = PromptValue(text=input_str)
        result = await self.agenerate(prompt, **kwargs)
        return result.generations[0].text