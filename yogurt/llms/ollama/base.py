import httpx
import json
from typing import Any, AsyncIterator, Iterator, List, Optional

from yogurt.llms.base import BaseLLM
from yogurt.output.base import Generation, LLMResult
from yogurt.output.streaming import StreamingChunk
from yogurt.prompts.prompt_value import PromptValue
from yogurt.messages.base import HumanMessage, AIMessage
from yogurt.callback_handlers.base import BaseCallbackHandler


class OllamaLLM(BaseLLM):
    """
    An LLM class that integrates with an Ollama service via direct API calls.
    """

    model_config = {
        "arbitrary_types_allowed": True,
    }

    host: str = "http://localhost:11434"

    # def __init__(self, callbacks: Optional[List[BaseCallbackHandler]] = None, **data: Any):
    #     super().__init__(**data)
    #     self.callbacks = callbacks or []

    def _invoke_callbacks(self, method_name: str, *args, **kwargs):
        """Helper to invoke a method on all callback handlers."""
        for handler in self.callbacks:
            if hasattr(handler, method_name):
                getattr(handler, method_name)(*args, **kwargs)

    def _build_payload(self, prompt: PromptValue, stream: bool, **kwargs: Any) -> dict:
        """Helper to construct the JSON payload for the Ollama API."""
        return {
            "model": self.model_name,
            "prompt": prompt.to_string(),
            "stream": stream,
            "options": {"temperature": self.temperature, **kwargs},
        }
    
    def _build_chat_payload(self, prompt: PromptValue, stream: bool, **kwargs: Any) -> dict:
        """Helper to construct the JSON payload for the /api/chat endpoint."""

        messages = [msg.model_dump_json() for msg in prompt.to_messages()]

        return {
            "model": self.model_name,
            "messages": messages,
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
            metadata=data,
        )
        return LLMResult(generations=[generation], llm_output=data)

    def invoke(self, input_str: str, **kwargs: Any) -> str:
        prompt = PromptValue(text=input_str, messages=[HumanMessage(content=input_str)])
        result = self.generate(prompt, **kwargs)
        return result.generations[0].text

    def stream(self, prompt: PromptValue, **kwargs: Any):
        """Streams a chat completion."""
        payload = self._build_chat_payload(prompt, stream=True, **kwargs)
        with httpx.Client() as client:
            with client.stream("POST", url = f"{self.host}/api/generate", json=payload, timeout=120) as response:
                for chunk in response.iter_lines():
                    chunk_data = json.loads(chunk)
                    print(f"\n[RAW CHUNK]: {chunk_data}")
                    yield chunk_data
                    # message_chunk = chunk_data.get("message", {})
                    # yield StreamingChunk(
                    #     text=message_chunk.get("content", ""),
                    #     metadata=chunk_data,
                    # )
                # for line in response.iter_lines():
                #     if line:
                #         chunk_data = json.loads(line)
                #         message_chunk = chunk_data.get("message", {})
                #         yield StreamingChunk(
                #             text=message_chunk.get("content", ""),
                #             metadata=chunk_data,
                #         )

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
            metadata=data,
        )
        return LLMResult(generations=[generation], llm_output=data)

    async def ainvoke(self, input_str: str, **kwargs: Any) -> str:
        prompt = PromptValue(text=input_str, messages=[HumanMessage(content=input_str)])
        result = await self.agenerate(prompt, **kwargs)
        return result.generations[0].text

    async def astream(
        self, prompt: PromptValue, **kwargs: Any
    ) -> AsyncIterator[StreamingChunk]:
        payload = self._build_chat_payload(prompt, stream=True, **kwargs)
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST", f"{self.host}/api/chat", json=payload, timeout=120
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        chunk_data = json.loads(line)
                        yield StreamingChunk(
                            text=chunk_data.get("response", ""),
                            metadata=chunk_data,
                        )
