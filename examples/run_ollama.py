import asyncio
from yogurt.llms.ollama import OllamaLLM
from yogurt.prompts.prompt_value import PromptValue

MODEL_NAME = "llama3.2:3b"


async def main():
    print(f"--- Using Model: {MODEL_NAME} ---")
    llm = OllamaLLM(model_name=MODEL_NAME, temperature=0.3)
    prompt = PromptValue(text="Tell me a short, three-line poem about the moon.")

    # --- Non-Streaming (Full Response at Once) ---
    print("\n--- Running Non-Streaming Generation ---")
    result = llm.generate(prompt)

    # result is an LLMResult object
    final_generation = result.generations[0]
    print("Final Text:")
    print(final_generation.text)
    print("\nGeneration Info:")
    final_nano = final_generation.metadata.get("total_duration")
    if final_nano:
        final_gen_secs = final_nano / 1_000_000_000
    # The 'generation_info' contains the full final response JSON from Ollama
    print(f"  - Total duration: {final_gen_secs} seconds")
    print(f"  - Eval count: {final_generation.metadata.get('eval_count')}")


if __name__ == "__main__":
    asyncio.run(main())
