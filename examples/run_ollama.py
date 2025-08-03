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
    result = llm.generate_prompt(prompt)

    # result is an LLMResult object
    final_generation = result.generations[0]
    print("Final Text:")
    print(final_generation.text)
    print("\nGeneration Info:")
    # The 'generation_info' contains the full final response JSON from Ollama
    print(
        f"  - Total duration: {final_generation.generation_info.get('total_duration')}"
    )
    print(f"  - Eval count: {final_generation.generation_info.get('eval_count')}")

    # --- Streaming (Chunks Arrive Over Time) ---
    print("\n\n--- Running Streaming Generation ---")

    full_response_text = ""
    final_chunk_info = {}

    stream = llm.stream(prompt)

    print("Streaming Text: ", end="")
    for chunk in stream:
        # chunk is a StreamingChunk object
        print(chunk.text, end="", flush=True)
        full_response_text += chunk.text

        # We can inspect the metadata of each chunk
        # Let's save the info from the last chunk, which has summary stats
        if chunk.chunk_info.get("done"):
            final_chunk_info = chunk.chunk_info

    print("\n\nStreaming Complete!")
    print(f"Final assembled text has {len(full_response_text)} characters.")
    print("Info from final chunk:")
    print(f"  - Total duration: {final_chunk_info.get('total_duration')}")
    print(f"  - Eval count: {final_chunk_info.get('eval_count')}")


if __name__ == "__main__":
    asyncio.run(main())
