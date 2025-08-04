import httpx
import json
from typing import Any, AsyncIterator, Iterator

# Use the consolidated BaseLLM
from yogurt.llms.base import BaseLLM
from yogurt.output.base import Generation, LLMResult
from yogurt.output.streaming import StreamingChunk
from yogurt.prompts.prompt_value import PromptValue
from yogurt.messages.base import AIMessage

class OllamaChat(BaseLLM):
    """
    An LLM class that integrates with the Ollama service using the /api/chat endpoint.
    """
    host: str = "http://localhost:11434"

    def _build_chat_payload(self, prompt: PromptValue, stream: bool, **kwargs: Any) -> dict:
        """Helper to construct the JSON payload for the /api/chat endpoint."""
        messages = [msg.model_dump() for msg in prompt.to_messages()]

        return {
            "model": self.model_name,
            "messages": messages,
            "stream": stream,
            "options": {"temperature": self.temperature, **kwargs},
        }

    def generate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """Generates a chat completion using the /api/chat endpoint."""
        payload = self._build_chat_payload(prompt, stream=False, **kwargs)
        
        with httpx.Client() as client:
            response = client.post(f"{self.host}/api/chat", json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()

        ai_message_data = data.get("message", {})
        ai_message = AIMessage(content=ai_message_data.get("content", ""))

        generation = Generation(
            text=ai_message.content,
            metadata=data, 
        )
        return LLMResult(generations=[generation], llm_output=data)

    # --- Override Optional Methods for Streaming ---
    def stream(self, prompt: PromptValue, **kwargs: Any) -> Iterator[StreamingChunk]:
        """Streams a chat completion."""
        payload = self._build_chat_payload(prompt, stream=True, **kwargs)
        with httpx.Client() as client:
            with client.stream("POST", f"{self.host}/api/chat", json=payload, timeout=120) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        chunk_data = json.loads(line)
                        message_chunk = chunk_data.get("message", {})
                        yield StreamingChunk(
                            text=message_chunk.get("content", ""),
                            # metadata=chunk_data,
                        )

    async def agenerate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """Asynchronously generates a chat completion."""
        payload = self._build_chat_payload(prompt, stream=False, **kwargs)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.host}/api/chat", json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
        
        ai_message_data = data.get("message", {})
        ai_message = AIMessage(content=ai_message_data.get("content", ""))
        
        generation = Generation(text=ai_message.content, metadata=data)
        return LLMResult(generations=[generation], llm_output=data)

    async def astream(
        self, prompt: PromptValue, **kwargs: Any
    ) -> AsyncIterator[StreamingChunk]:
        """Asynchronously streams a chat completion."""
        payload = self._build_chat_payload(prompt, stream=True, **kwargs)
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", f"{self.host}/api/chat", json=payload, timeout=120) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        chunk_data = json.loads(line)
                        message_chunk = chunk_data.get("message", {})
                        yield StreamingChunk(
                            text=message_chunk.get("content", ""),
                            metadata=chunk_data,
                        )