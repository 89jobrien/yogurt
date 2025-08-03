import httpx
import json
from typing import Any, AsyncIterator, Iterator

from yogurt.llms.base import BaseLLM
from yogurt.output.base import Generation, LLMResult
from yogurt.output.streaming import StreamingChunk
from yogurt.prompts.prompt_value import PromptValue
from yogurt.messages.base import HumanMessage


class OllamaLLM(BaseLLM):
    """
    An LLM class that integrates with an Ollama service via direct API calls.
    """

    model_config = {
        "arbitrary_types_allowed": True,
    }

    host: str = "http://localhost:11434"

    def _build_payload(self, prompt: PromptValue, stream: bool, **kwargs: Any) -> dict:
        """Helper to construct the JSON payload for the Ollama API."""
        return {
            "model": self.model_name,
            "prompt": prompt.to_string(),
            "stream": stream,
            "options": {"temperature": self.temperature, **kwargs},
        }

    def _generate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        payload = self._build_payload(prompt, stream=False, **kwargs)
        with httpx.Client() as client:
            response = client.post(
                f"{self.host}/api/generate", json=payload, timeout=120
            )
            response.raise_for_status()
            data = response.json()

        generation = Generation(
            text=data.get("response", ""),
            generation_info=data,
        )
        return LLMResult(generations=[generation], llm_output=data)

    def generate_prompt(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        return self._generate(prompt, **kwargs)

    def invoke(self, input_str: str, **kwargs: Any) -> str:
        prompt = PromptValue(text=input_str, messages=[HumanMessage(content=input_str)])
        result = self.generate_prompt(prompt, **kwargs)
        return result.generations[0].text

    def stream(self, prompt: PromptValue, **kwargs: Any) -> Iterator[StreamingChunk]:
        payload = self._build_payload(prompt, stream=True, **kwargs)
        with httpx.Client() as client:
            with client.stream(
                "POST", f"{self.host}/api/generate", json=payload, timeout=120
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        chunk_data = json.loads(line)
                        yield StreamingChunk(
                            text=chunk_data.get("response", ""),
                            chunk_info=chunk_data,
                        )

    async def agenerate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        payload = self._build_payload(prompt, stream=False, **kwargs)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.host}/api/generate", json=payload, timeout=120
            )
            response.raise_for_status()
            data = response.json()

        generation = Generation(
            text=data.get("response", ""),
            generation_info=data,
        )
        return LLMResult(generations=[generation], llm_output=data)

    async def ainvoke(self, input_str: str, **kwargs: Any) -> str:
        prompt = PromptValue(text=input_str, messages=[HumanMessage(content=input_str)])
        result = await self.agenerate(prompt, **kwargs)
        return result.generations[0].text

    async def astream(
        self, prompt: PromptValue, **kwargs: Any
    ) -> AsyncIterator[StreamingChunk]:
        payload = self._build_payload(prompt, stream=True, **kwargs)
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", f"{self.host}/api/generate", json=payload, timeout=120
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        chunk_data = json.loads(line)
                        yield StreamingChunk(
                            text=chunk_data.get("response", ""),
                            chunk_info=chunk_data,
                        )
