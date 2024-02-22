#!/usr/bin/env python3
import os

from chat import Client
from chat.language_model import GPT, LLM, OLLAMA


def get_model(lm):
    if lm == LLM.GPT4:
        if not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
            print("OPENAI_API_KEY not set!")
            exit()
        return GPT()

    elif lm == LLM.DOLPHIN_MIXTRAL:
        return OLLAMA(lm)
    return OLLAMA()


def app():
    tui = Client()
    tui.run()


if __name__ == "__main__":
    app()
