import asyncio
from yogurt.llms.ollama.chat import OllamaChat
from yogurt.callback_handlers.stdout import StdOutCBH, StreamedStdOutCBH
from yogurt.pipes.llm.llm_pipe import LLMPipe
from yogurt.prompts.builders.chat import ChatPromptBuilder

# Make sure you have this model pulled, e.g., `ollama pull qwen2:0.5b`
MODEL_NAME = "gemma3:4b"


async def main():
    """Demonstrates a pure streaming workflow where callbacks handle all output."""

    # 1. Instantiate both callback handlers
    stdout_handler = StdOutCBH()
    streaming_handler = StreamedStdOutCBH()

    # 2. Instantiate the LLM
    llm = OllamaChat(model_name=MODEL_NAME, temperature=0.3)

    # 3. Use the ChatPromptBuilder
    chat_prompt = ChatPromptBuilder(
        system_msg=(
            "You are a code generation bot. You will be given a task to write a "
            "program in {language}. You must respond with ONLY the raw code for the "
            "solution, and nothing else. Do not add any conversational text, "
            "explanations, or markdown formatting."
        ),
        human_msg="{task}",
    )

    # 4. Assemble the LLMPipe
    pipe = LLMPipe(
        prompt=chat_prompt, llm=llm, callbacks=[stdout_handler, streaming_handler]
    )

    # 5. Run the stream and let the callbacks handle the output
    print("\n--- Streaming Translation ---")
    # print(chat_prompt)

    # We simply consume the async iterator to drive the stream.
    # The `StreamedStdOutCBH` callback handles all the real-time printing.
    async for _ in pipe.astream(
        language="python",
        task="Write the full code for a function that finds the nth fibonacci number",
    ):
        pass

    # Add a final newline for clean formatting after the stream is done.
    print()


if __name__ == "__main__":
    asyncio.run(main())
