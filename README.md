# 🍦Yogurt

## [Under Construction]

A fresh, type-safe, and modular AI framework for building powerful language applications in Python.

Yogurt provides the essential, composable building blocks for creating applications with LLMs. It is designed with a strong emphasis on developer experience, using modern Python features and robust type-safety to make your code predictable, reliable, and easy to extend.

## Key Features

- **Type-Safe by Design**: Leverages Pydantic for all data models and configuration, ensuring that data flowing through your pipes and components is always valid.

- **Modular Components**: The framework is built on a set of clear interfaces (`BaseLLM`, `BasePipe`, etc.), allowing you to easily implement and swap out components.

- **Async & Streaming Native**: Built from the ground up with first-class support for async and streaming operations, making it suitable for high-performance, real-time applications.

- **Extensible Interfaces**: Add your own LLM providers, prompt strategies, or parsers by simply inheriting from the provided abstract base classes.

- **Minimal Dependencies**: Keeps the core light and fast, only requiring pydantic and httpx for its main functionality.

---

## Installation

To get started with 🍦Yogurt: 

1. Initialize your virtual environment:

```bash
uv venv
source .venv/bin/activate
```

2. Clone the repository and install it with `uv`:

```bash
git clone https://github.com/89jobrien/yogurt.git
cd yogurt
uv sync
```
```bash
# To install 🍦Yogurt in editable mode:
uv pip install -e .
```

This will install the package along with its core dependencies:
- `pydantic`
- `httpx`

You may need to install additional libraries for specific integrations (e.g., `ollama`).

[Download Ollama](https://ollama.com/)

After installing `ollama`:

```bash
ollama pull llama3.2:3b
```

Run the local inference server:

```bash
ollama serve
```

Here is a basic script to use 🍦Yogurt with Ollama:

```python
import asyncio
from yogurt.llms.ollama import OllamaLLM
from yogurt.prompts.base import PromptValue

MODEL_NAME = "llama3.2:3b"

async def main():
    print(f"--- Using Model: {MODEL_NAME} ---")
    llm = OllamaLLM(model_name=MODEL_NAME, temperature=0.3)
    prompt = PromptValue(text="Tell me a short, three-line poem about a river.")

    # --- Streaming (Chunks Arrive Over Time) ---
    print("\n--- Running Streaming Generation ---")
    
    full_response_text = ""
    stream = llm.stream(prompt)
    
    print("Streaming Text: ", end="")
    for chunk in stream:
        # 'chunk' is a structured StreamingChunk object
        print(chunk.text, end="", flush=True)
        full_response_text += chunk.text
            
    print("\n\nStreaming Complete!")
    print(f"Final assembled text has {len(full_response_text)} characters.")

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Concepts

#### LLMs
These are wrappers around language models from various providers. The BaseLLM interface defines a standard contract for interacting with any model, including methods for synchronous, asynchronous, and streaming calls.

#### Prompts
Prompt templates manage the construction of prompts sent to LLMs. They allow for dynamic input and can be composed to handle complex prompting scenarios.

#### Pipes
Pipes are the core of the framework, allowing you to combine components (like prompts, LLMs, and parsers) into a single, executable sequence. The LLMPipe is the most fundamental example.

#### Output Models
Yogurt uses explicit Pydantic models for LLM outputs to ensure clarity and type safety.

#### Generation
Represents the final, complete output from a non-streaming LLM call.

#### StreamingChunk
Represents a single, discrete piece of a streaming response, containing both text and metadata.

#### Memory
Memory components give pipes and agents the ability to remember past interactions, enabling stateful, conversational applications.

## Roadmap

Yogurt is under active development with the goal of providing a comprehensive, modular, and type-safe framework for building AI agents and language applications in Python. Our planned roadmap includes:

- **v0.1 - Core Foundations**
  - Define core interfaces and abstract base classes for LLMs, Pipes, Agents, Tools, and Memory modules  
  - Build type-safe prompt templates with Pydantic validation

- **v0.2 - Extensibility and Integrations**
  - Expand support for more LLM providers and integrate vector database retrievers for retrieval augmented generation (RAG)
  - Introduce modular toolkits and plugin systems for composing custom agent workflows
  - Add output parsing utilities for structured extraction from LLM results
  - Improve memory modules to support long-term conversation context management

- **v0.3 - Advanced Agent Capabilities**
  - Develop autonomous decision-making agents capable of selecting tools and pipes dynamically
  - Support multi-agent collaboration and orchestration
  - Enhance async/streaming capabilities across the framework for high-performance real-time applications
  - Provide SDK enhancements for simplified development and deployment  

- **v1.0 - Production Ready & Ecosystem Growth**
  - Stabilize APIs with backward-compatible improvements
  - Build detailed documentation, tutorials, and example applications
  - Encourage community contributions, third-party integrations, and ecosystem toolkits
  - Explore GUI and low-code interfaces for non-developers
