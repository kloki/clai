import asyncio

from ollama import AsyncClient as OllamaClient
from openai import AsyncOpenAI as OpenAIClient


class OpenAI:

    def __init__(self, name="gpt-4", temperature=1, top_p=1):
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

    def __init__(self, name="dolphin-mistral"):
        self.name = name
        self.icon = "🐬"

    async def query(self, session):
        stream = OllamaClient().chat(
            model=self.name, messages=session.payload(), stream=True
        )
        async for chunk in await stream:
            yield chunk["message"]["content"]


class Dummy:

    def __init__(self):
        self.name = "dummy"
        self.icon = "🗑️"

    async def query(self, session):
        for i in ["1", "...", "2", "...", "Done"]:
            await asyncio.sleep(0.0)
            yield i
