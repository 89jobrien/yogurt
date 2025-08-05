import asyncio
from yogurt.llms.ollama import OllamaChat
from yogurt.callback_handlers.stdout import StdOutCBH, StreamedStdOutCBH
from yogurt.pipes.llm.llm_pipe import LLMPipe
from yogurt.prompts.builders.chat import ChatPromptBuilder


MODEL_NAME = "qwen2:0.5b"

async def main():
    """Demonstrates the streaming conversational chat workflow."""

    # 1. Instantiate BOTH callback handlers
    stdout_handler = StdOutCBH()
    streaming_handler = StreamedStdOutCBH()

    # 2. Instantiate the LLM
    llm = OllamaChat(model_name=MODEL_NAME, temperature=0.3, callbacks=[stdout_handler, streaming_handler])

    # 3. Use the ChatPromptBuilder
    chat_prompt = ChatPromptBuilder(
        system_msg="You are a helpful assistant who translates English to {language}.",
        human_msg="Translate this sentence: {sentence}"
    )

    # 4. Assemble the LLMPipe, passing in BOTH handlers
    pipe = LLMPipe(
        prompt=chat_prompt,
        llm=llm,
        callbacks=[stdout_handler, streaming_handler]
    )

    # 5. Run the stream and collect the final result.
    print("\n--- Streaming Translation ---")
    
    final_result_parts = [
        chunk.text async for chunk in pipe.astream(
            language="French",
            sentence="I love programming and building modular AI frameworks."
        )
    ]
    final_result = "".join(final_result_parts)

    # 6. Print the fully assembled result after the stream is complete
    print("\n\n--- Final Assembled Translation ---")
    print(final_result)


if __name__ == "__main__":
    asyncio.run(main())