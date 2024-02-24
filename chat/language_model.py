import asyncio

import requests
from openai import OpenAI


class OpenAIClient:

    def __init__(self, name="gpt-4", temperature=1, top_p=1):
        self.temperature = temperature
        self.top_p = top_p
        self.client = OpenAI()
        self.name = name
        self._settings = self.settings()
        self.icon = "🧠"

    def settings(self):
        return {
            "model": self.name,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }

    def query(self, session):
        response = self.client.chat.completions.create(
            messages=session.payload(), **self._settings
        )
        return response.choices[0].message.content


class Ollama:

    def __init__(self, name="dolphin-mistral"):
        self.name = name
        self.url = "http://127.0.0.1:11434/api/chat"
        self.icon = "🐬"

    def query(self, session):
        payload = {"model": self.name, "messages": session.payload(), "stream": False}
        response = requests.post(self.url, json=payload)
        return response.json()["message"]["content"]


class Dummy:

    def __init__(self):
        self.name = "dummy"
        self.icon = "🗑️"

    async def query(self, session):
        for i in ["1", "1...", "2...", "Done"]:
            await asyncio.sleep(0.5)
            yield i
