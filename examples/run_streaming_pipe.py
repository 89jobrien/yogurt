import asyncio
from yogurt.llms.ollama import OllamaChat
from yogurt.callback_handlers.stdout import StdOutCBH, StreamedStdOutCBH
from yogurt.pipes.llm.llm_pipe import LLMPipe
from yogurt.prompts.builders.chat import ChatPromptBuilder
from yogurt.parsers.output_parsers.json import JsonResponseParser

# Make sure you have this model pulled, e.g., `ollama pull llama3.2:3b`
MODEL_NAME = "llama3.2:3b"

async def main():
    """Demonstrates using astream and then parsing the final result."""
    
    # 1. Setup handlers and the JSON parser
    stdout_handler = StdOutCBH()
    streaming_handler = StreamedStdOutCBH()
    json_parser = JsonResponseParser()

    # 2. Instantiate the LLM
    llm = OllamaChat(model_name=MODEL_NAME, temperature=0.1)

    # 3. Create a prompt with JSON formatting instructions
    chat_prompt = ChatPromptBuilder(
        system_msg=f"You are a helpful assistant.",
        human_msg="Create a short conversation about the user's topic: {topic}"
    )

    # 4. Assemble the pipe, but WITHOUT the parser initially
    pipe = LLMPipe(
        prompt=chat_prompt,
        llm=llm,
        callbacks=[stdout_handler, streaming_handler],
        # The output_parser is not passed to the pipe for streaming
    )

    # 5. Stream the response and collect the text
    print("\n--- Streaming Raw Chunks ---")

    async for chunk in pipe.astream(topic="learning to code"):
        parsed_msgs = json_parser.parse_chunk(chunk)
        for message in parsed_msgs:
            print(f"\n[PARSED MESSAGE]: Role={message.role}, Content='{message.content}'")

    # # 6. Now, parse the complete text
    # print("\n\n--- Parsing Final Assembled Text ---")
    # parsed_result = json_parser.parse(final_raw_text)

    # # 7. Print the final, structured result
    # print("\n--- Final Parsed Output ---")
    # for message in parsed_result:
    #     print(f"  - Role: {message.role}, Content: '{message.content}'")

if __name__ == "__main__":
    asyncio.run(main())