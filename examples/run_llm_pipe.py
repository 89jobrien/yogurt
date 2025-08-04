import asyncio
from yogurt.llms.ollama import OllamaLLM
from yogurt.prompts.prompt_value import PromptValue
from yogurt.callback_handlers.stdout import StdOutCBH, StreamedStdOutCBH
from yogurt.output.base import LLMResult
from yogurt.parsers.output_parsers import OutputParser
from yogurt.pipes.llm.llm_pipe import LLMPipe
from yogurt.prompts.builders import PromptBuilder
from yogurt.prompts.builders.chat import ChatPromptBuilder

# Make sure you have this model pulled, e.g., `ollama pull llama3`
MODEL_NAME = "llama3.2:3b" 

async def main():
    """Demonstrates the new conversational chat workflow."""
    
    # 1. Setup the LLM and callbacks
    llm = OllamaLLM(model_name=MODEL_NAME)
    stdout_handler = StdOutCBH()

    # 2. Use the new ChatPromptBuilder
    chat_prompt = ChatPromptBuilder(
        system_msg="You are a helpful assistant who translates English to {language}.",
        human_msg="Translate this sentence: {sentence}"
    )

    # 3. Assemble the simplified LLMPipe
    pipe = LLMPipe(
        prompt=chat_prompt,
        llm=llm,
        callbacks=[stdout_handler]
    )

    # 4. Run the pipe with dynamic inputs
    result = pipe.run(language="French", sentence="I love programming.")

    # 5. Print the final result
    print("\n--- Final Translation ---")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())