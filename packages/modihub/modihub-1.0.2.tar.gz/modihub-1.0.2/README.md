# MODIHUB: A Unified Interface for Diverse LLMs

**MODIHUB** simplifies the way you interact with multiple Large Language Models (LLMs) by offering a streamlined, consistent interface. It abstracts the complexities of provider-specific APIs and configurations, making it easy to switch between models across different platforms.

## 🔑 Key Features

- **Unified API:** Seamlessly interact with models from OpenAI, Gemini, Anthropic, Ollama, Groq, and more using a consistent interface.
- **Model Discovery:** Effortlessly list and explore available models from each provider.
- **Multimodal Support:** Work with text, image, and mixed-modality prompts where supported.
- **Built-in Evaluation Tools:** Evaluate model performance with utilities for perplexity, lexical diversity, and more.

## Installation

```bash
pip install -U modihub
```

## Usage Examples

### 1. Listing Available Models

```python
from modihub.llm import LLM

available_models = LLM.available_models()
for client, models in available_models.group_by("client"):
    print(f"{client}:")
    for model in models:
        print(f"  - {model.name}")
```

### 2. Text Generation

```python
from modihub.llm import LLM
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv()) # Loads API keys from .env file

# Replace with your desired model
llm = LLM.create("gpt-4o-mini")
# Generate text
response = llm("Tell me a joke about AI.")
print(response)
```

### 3. Multimodal Input (Image Description)

```python
from PIL import Image
from modihub.llm import LLM
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
# Replace with your desired model
llm = LLM.create("models/gemini-1.5-flash-8b")
# Load image
image = Image.open("image.png")  # Replace with the path to your image
text = "Describe the following image"
# create multimodal prompt
prompt = [text, image]
response = llm(prompt)
print(response)
```

### 4. Model Evaluation (Pointwise Metrics)

```python
from dotenv import find_dotenv, load_dotenv
from modihub.metrics import Perplexity, LexicalDiversity
from modihub.eval import Evaluator

load_dotenv(find_dotenv())

prompts = [
    "What are LLMs?",
    "Explain AI", "What is the meaning of life?"]
models = [
    "gpt-4o-mini",
    "llama3.1:latest",
    "models/gemini-1.5-flash-latest"
]
metrics = [Perplexity(), LexicalDiversity()]

evaluator = Evaluator(models, metrics)
results = {prompt: evaluator.evaluate(prompt) for prompt in prompts}
for prompt, result in results.items():
    print(f"Prompt: {prompt}")
    for model, metrics in zip(models, result):
        print(f"{model}: {metrics}")
    print()
```

## Configuration

*   **API Keys:** Set your API keys for each LLM provider as environment variables (e.g., `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, or `GROQ_API_KEY`).  A `.env` file in your project directory is a good place to store these.
*   **Support Clients:** MODI currently supports OpenAI, Gemini, Anthropic, Ollama, and Groq models.  You can add support for additional clients by implementing the `LLMClient` interface.
*   **System Instructions:**  Use the `system_instruction` parameter when creating an LLM instance to provide context or instructions to the model.  This is supported by all clients.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

[MIT License](LICENSE)  (Include a `LICENSE` file in your repository containing the MIT License text.)

