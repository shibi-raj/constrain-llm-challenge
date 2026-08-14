from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


def create_llm(provider: str, model: str):
    if provider == "ollama":
        return ChatOllama(
            model=model,
            temperature=0,
        )

    if provider == "openrouter":
        return ChatOpenAI(
            model=model,
            temperature=0,
            base_url="https://openrouter.ai/api/v1",
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")