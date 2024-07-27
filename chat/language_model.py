import asyncio

from anthropic import AsyncAnthropic as AnthropicClient
from ollama import AsyncClient as OllamaClient
from openai import AsyncOpenAI as OpenAIClient


class OpenAI:
    def __init__(self, name="gpt-4o-mini", temperature=1, top_p=1):
        self.temperature = temperature
        self.top_p = top_p
        self.client = OpenAIClient()
        self.name = name
        self._settings = self.settings()
        self.icon = "🧠"

    def settings(self):
        return {
            "model": self.name,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": True,
        }

    async def query(self, session):
        stream = await self.client.chat.completions.create(
            messages=session.payload(), **self._settings
        )
        async for chunk in stream:
            yield chunk.choices[0].delta.content or ""


class Ollama:
    def __init__(self, name="llama2", icon="🦙"):
        self.name = name
        self.icon = icon
        self.client = OllamaClient()

    async def query(self, session):
        stream = self.client.chat(
            model=self.name, messages=session.payload(), stream=True
        )
        async for chunk in await stream:
            yield chunk["message"]["content"]


class Anthropic:
    def __init__(self, name="claude-3-opus-20240229", icon="🙆"):
        self.name = name
        self.icon = icon
        self.client = AnthropicClient()

    async def query(self, session):
        system, payload = session.payload_anthropic()
        stream = await self.client.messages.create(
            model=self.name,
            messages=payload,
            system=system,
            stream=True,
            max_tokens=1024,
        )
        async for event in stream:
            if event.type == "content_block_delta":
                yield event.delta.text


class Dummy:
    def __init__(self):
        self.name = "dummy"
        self.icon = "🗑️"

    async def query(self, session):
        for i in ["1", "...", "2", "...", "Done"]:
            await asyncio.sleep(0.0)
            yield i


LLM = {
    "dolphin": Ollama("dolphin-llama3", icon="🐬"),
    "tinydolphin": Ollama("tinydolphin", icon="🐬🤏"),
    "bigdolphin": Ollama("dolphin-mistral:7b-v2.8-fp16", icon="🐬💪"),
    "gpt": OpenAI(),
    "anthropic": Anthropic(),
}

LLM_ORDER = list(LLM.values())


def get_next_llm(model):
    index = LLM_ORDER.index(model) + 1
    return LLM_ORDER[index % len(LLM_ORDER)]
