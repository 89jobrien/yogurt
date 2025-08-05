import asyncio
from yogurt.llms.ollama import OllamaLLM
from yogurt.prompts.builders.chat import ChatPromptBuilder

MODEL_NAME = "llama3.2:3b"


async def main():
    """
    Demonstrates a robust, non-streaming request to the Ollama /api/generate
    endpoint using the dedicated system prompt parameter.
    """
    print(f"--- Using Model: {MODEL_NAME} with raw=True and dedicated system prompt ---")

    # Use the OllamaLLM class, which is designed for the /api/generate endpoint
    # Set temperature to 0.0 for more deterministic, predictable output
    llm = OllamaLLM(model_name=MODEL_NAME, temperature=0.0)

    # Use ChatPromptBuilder to clearly separate the system and human messages.
    prompt_builder = ChatPromptBuilder(
        system_msg="You are a helpful and creative poet who only responds with the poem itself.",
        human_msg="Tell me a short, three-line poem about the moon."
    )

    # The builder creates a PromptValue object with the structured messages
    prompt_value = prompt_builder.format_prompt()

    # --- Running Non-Streaming Generation ---
    print("\n--- Running Non-Streaming Generation ---")
    result = llm.generate(prompt_value)

    # result is an LLMResult object containing the full response
    final_generation = result.generations[0]

    print("\n--- Final Text ---")
    print(final_generation.text)

    print("\n--- Generation Info ---")
    metadata = final_generation.metadata
    
    # The 'total_duration' from Ollama is in nanoseconds; we convert it to seconds.
    total_duration_ns = metadata.get("total_duration")
    if total_duration_ns:
        duration_s = total_duration_ns / 1_000_000_000
        print(f"  - Total duration: {duration_s:.2f} seconds")
    
    print(f"  - Eval count: {metadata.get('eval_count')}")


if __name__ == "__main__":
    asyncio.run(main())