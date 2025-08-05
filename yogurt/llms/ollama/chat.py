import httpx
import json
from typing import Any, AsyncIterator, Iterator, List, Optional, Dict

# Inherit from the base OllamaLLM class
from .base import OllamaLLM
from yogurt.output.base import Generation, LLMResult
from yogurt.output.streaming import StreamingChunk
from yogurt.prompts.prompt_value import PromptValue
from yogurt.messages.base import AIMessage
from yogurt.tools.base import BaseTool
from yogurt.types.api import APIRequest, APIResponse


class OllamaChat(OllamaLLM):
    """
    An LLM class that integrates with the Ollama service using the /api/chat endpoint.
    It overrides the payload creation and API calling methods from OllamaLLM to
    handle conversational message structures.
    """

    def _build_chat_payload(
        self,
        prompt: PromptValue,
        stream: bool,
        tools: Optional[List[BaseTool]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Helper to construct the JSON payload for the /api/chat endpoint."""
        messages = [msg.model_dump() for msg in prompt.to_messages()]

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": stream,
            "options": {"temperature": self.temperature, **kwargs},
        }

        if tools:
            payload["tools"] = [tool.get_schema() for tool in tools]
        
        print("\n--- Sending Payload to Ollama /api/chat ---")
        print(json.dumps(payload, indent=2))
        print("---------------------------------")
        return payload

    def _generate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """Generates a chat completion using the /api/chat endpoint."""
        payload = self._build_chat_payload(prompt, stream=False, **kwargs)
        request = APIRequest(
            method="POST",
            url=f"{self.host}/api/chat",
            body=payload,
        )

        with httpx.Client() as client:
            response = client.request(
                method=request.method,
                url=request.url,
                json=request.body,
                timeout=120,
            )
            response.raise_for_status()
            api_response = APIResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
                body=response.json(),
            )
        data = api_response.body

        ai_message_data = data.get("message", {})
        ai_message = AIMessage(content=ai_message_data.get("content", ""))

        generation = Generation(
            text=ai_message.content,
            metadata=data,
        )
        return LLMResult(generations=[generation], llm_output=data)

    def stream(self, prompt: PromptValue, **kwargs: Any) -> Iterator[StreamingChunk]:
        """Streams a chat completion from the /api/chat endpoint."""
        payload = self._build_chat_payload(prompt, stream=True, **kwargs)
        request = APIRequest(
            method="POST",
            url=f"{self.host}/api/chat",
            body=payload,
        )
        with httpx.Client() as client:
            with client.stream(
                method=request.method,
                url=request.url,
                json=request.body,
                timeout=120
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        chunk_data = json.loads(line)
                        message_chunk = chunk_data.get("message", {})
                        yield StreamingChunk(
                            text=message_chunk.get("content", ""),
                            metadata=chunk_data,
                        )

    async def agenerate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
        """Asynchronously generates a chat completion using the /api/chat endpoint."""
        payload = self._build_chat_payload(prompt, stream=False, **kwargs)
        request = APIRequest(
            method="POST",
            url=f"{self.host}/api/chat",
            body=payload,
        )
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=request.url,
                json=request.body,
                timeout=120,
            )
            response.raise_for_status()
            api_response = APIResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
                body=await response.json(),
            )
        data = api_response.body

        ai_message_data = data.get("message", {})
        ai_message = AIMessage(content=ai_message_data.get("content", ""))

        generation = Generation(text=ai_message.content, metadata=data)
        return LLMResult(generations=[generation], llm_output=data)

    async def astream(
        self, prompt: PromptValue, **kwargs: Any
    ) -> AsyncIterator[StreamingChunk]:
        """Asynchronously streams a chat completion from the /api/chat endpoint."""
        payload = self._build_chat_payload(prompt, stream=True, **kwargs)
        request = APIRequest(
            method="POST",
            url=f"{self.host}/api/chat",
            body=payload,
        )
        async with httpx.AsyncClient() as client:
            async with client.stream(
                method=request.method,
                url=request.url,
                json=request.body,
                timeout=120,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        chunk_data = json.loads(line)
                        message_chunk = chunk_data.get("message", {})
                        yield StreamingChunk(
                            text=message_chunk.get("content", ""),
                            metadata=chunk_data,
                        )

# import httpx
# import json
# from typing import Any, AsyncIterator, Iterator, List, Optional, Dict

# # Use the consolidated BaseLLM
# from yogurt.llms.ollama import OllamaLLM
# from yogurt.output.base import Generation, LLMResult
# from yogurt.output.streaming import StreamingChunk
# from yogurt.prompts.prompt_value import PromptValue
# from yogurt.messages.base import AIMessage
# from yogurt.tools.base import BaseTool
# from yogurt.types.api import APIRequest, APIResponse


# class OllamaChat(OllamaLLM):
#     """
#     An LLM class that integrates with the Ollama service using the /api/chat endpoint.
#     """

#     host: str = "http://localhost:11434"

#     def _build_chat_payload(
#         self,
#         prompt: PromptValue,
#         stream: bool,
#         tools: Optional[List[BaseTool]] = None,
#         **kwargs: Any
#     ) -> Dict[str, Any]:
#         """Helper to construct the JSON payload for the /api/chat endpoint."""
#         messages = [msg.model_dump() for msg in prompt.to_messages()]

#         payload = {
#             "model": self.model_name,
#             "messages": messages,
#             "stream": stream,
#             "options": {"temperature": self.temperature, **kwargs},
#         }

#         if tools:
#             payload["tools"] = [tool.get_schema() for tool in tools]

#         print("\n--- Sending Payload to Ollama ---")
#         print(json.dumps(payload, indent=2))
#         print("---------------------------------")
#         return payload

#     def _generate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
#         """Generates a chat completion using the /api/chat endpoint."""
#         payload = self._build_chat_payload(prompt, stream=False, **kwargs)
#         request = APIRequest(
#             method="POST",
#             url=f"{self.host}/api/chat",
#             body=payload,
#         )

#         with httpx.Client() as client:
#             response = client.request(
#                 method=request.method,
#                 url=request.url,
#                 json=request.body,
#                 timeout=120,
#             )
#             response.raise_for_status()
#             api_response = APIResponse(
#                 status_code=response.status_code,
#                 headers=dict(response.headers),
#                 body=response.json(),
#             )
#         data = api_response.body

#         ai_message_data = data.get("message", {})
#         ai_message = AIMessage(content=ai_message_data.get("content", ""))

#         generation = Generation(
#             text=ai_message.content,
#             metadata=data,
#         )
#         return LLMResult(generations=[generation], llm_output=data)

#     def stream(self, prompt: PromptValue, **kwargs: Any) -> Iterator[StreamingChunk]:
#         """Streams a chat completion."""
#         payload = self._build_chat_payload(prompt, stream=True, **kwargs)
#         request = APIRequest(
#             method="POST",
#             url=f"{self.host}/api/chat",
#             body=payload,
#         )
#         with httpx.Client() as client:
#             with client.stream(
#                 method=request.method,
#                 url=request.url,
#                 json=request.body,
#                 timeout=120
#             ) as response:
#                 response.raise_for_status()
#                 for line in response.iter_lines():
#                     if line:
#                         chunk_data = json.loads(line)
#                         # print(f"\n[RAW CHUNK]: {chunk_data}")
#                         message_chunk = chunk_data.get("message", {})
#                         yield StreamingChunk(
#                             text=message_chunk.get("content", ""),
#                             metadata=chunk_data,
#                         )

#     async def agenerate(self, prompt: PromptValue, **kwargs: Any) -> LLMResult:
#         """Asynchronously generates a chat completion."""
#         payload = self._build_chat_payload(prompt, stream=False, **kwargs)
#         request = APIRequest(
#             method="POST",
#             url=f"{self.host}/api/chat",
#             body=payload,
#         )
#         async with httpx.AsyncClient() as client:
#             response = await client.request(
#                 method=request.method,
#                 url=request.url,
#                 json=request.body,
#                 timeout=120,
#             )
#             response.raise_for_status()
#             api_response = APIResponse(
#                 status_code=response.status_code,
#                 headers=dict(response.headers),
#                 body=await response.json(),
#             )
#         data = api_response.body

#         ai_message_data = data.get("message", {})
#         ai_message = AIMessage(content=ai_message_data.get("content", ""))

#         generation = Generation(text=ai_message.content, metadata=data)
#         return LLMResult(generations=[generation], llm_output=data)

#     async def astream(
#         self, prompt: PromptValue, **kwargs: Any
#     ) -> AsyncIterator[StreamingChunk]:
#         """Asynchronously streams a chat completion."""
#         payload = self._build_chat_payload(prompt, stream=True, **kwargs)
#         request = APIRequest(
#             method="POST",
#             url=f"{self.host}/api/chat",
#             body=payload,
#         )
#         async with httpx.AsyncClient() as client:
#             async with client.stream(
#                 method=request.method,
#                 url=request.url,
#                 json=request.body,
#                 timeout=120,
#             ) as response:
#                 response.raise_for_status()
#                 async for line in response.aiter_lines():
#                     if line:
#                         chunk_data = json.loads(line)
#                         # print(f"\n[RAW CHUNK]: {chunk_data}")
#                         message_chunk = chunk_data.get("message", {})
#                         yield StreamingChunk(
#                             text=message_chunk.get("content", ""),
#                             metadata=chunk_data,
#                         )