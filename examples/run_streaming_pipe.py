import asyncio
from yogurt.llms.ollama.chat import OllamaChat
from yogurt.callback_handlers.stdout import StdOutCBH, StreamedStdOutCBH
from yogurt.pipes.llm.llm_pipe import LLMPipe
from yogurt.prompts.builders.chat import ChatPromptBuilder

# Make sure you have this model pulled, e.g., `ollama pull qwen2:0.5b`
MODEL_NAME = "qwen2.5-coder:0.5b"


async def main():
    """
    Demonstrates a streaming workflow using the OllamaChat class, which is
    the correct implementation for conversational, multi-message prompts.
    """

    # 1. Instantiate both callback handlers
    stdout_handler = StdOutCBH()
    streaming_handler = StreamedStdOutCBH()

    # 2. Instantiate the OllamaChat LLM
    # We set temperature to 0.0 for more predictable, deterministic code generation.
    llm = OllamaChat(model_name=MODEL_NAME, temperature=0.0)

    # 3. Use the ChatPromptBuilder to create a structured list of messages
    chat_prompt = ChatPromptBuilder(
        system_msg=(
            "You are an expert Python code generation bot. "
            "You must respond with ONLY the raw Python code for the requested function. "
            "Do not provide any explanations, introductory text, or markdown formatting."
        ),
        human_msg=(
            "You are an expert Python code generation bot. "
            "You must respond with ONLY the raw Python code for the requested function. "
            "Do not provide any explanations, introductory text, or markdown formatting."
            "Write a single Python function named `fibonacci` that takes one integer "
            "argument `n` and returns the nth Fibonacci number."
        ),
    )

    # 4. Assemble the LLMPipe with the OllamaChat instance
    pipe = LLMPipe(
        prompt=chat_prompt, llm=llm, callbacks=[stdout_handler, streaming_handler]
    )

    # 5. Run the stream.
    print(f"\n--- Generating code with {MODEL_NAME} using the /api/chat endpoint ---")

    # The pipe will call llm.astream(), which correctly sends the messages
    # to the /api/chat endpoint.
    async for _ in pipe.astream():
        pass

    print("\n\n--- Generation Complete ---")


if __name__ == "__main__":
    asyncio.run(main())
