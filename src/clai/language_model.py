import asyncio

from openai import AsyncOpenAI as OpenAIClient

from .dummy_answers import PAYLOAD


class OpenAI:
    def __init__(self, name="gpt-4o-mini", icons="🧠", temperature=1, top_p=1):
        self.temperature = temperature
        self.top_p = top_p
        self.client = OpenAIClient()
        self.name = name
        self._settings = self.settings()
        self.icon = icons

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


class Dummy:
    def __init__(self):
        self.name = "dummy"
        self.icon = "🗑️"

    async def query(self, session):
        for i in PAYLOAD:
            await asyncio.sleep(0.2)
            yield i


LLM = {
    "gpt": OpenAI(),
    "o1": OpenAI("o1-mini", icons="🧬"),
    # "dummy": Dummy(),
}

LLM_ORDER = list(LLM.values())


def get_next_llm(model):
    index = LLM_ORDER.index(model) + 1
    return LLM_ORDER[index % len(LLM_ORDER)]
