#!/usr/bin/env python3
import enum
import os

import typer
from rich import print

from chat import Chat
from chat.assistant import ASSISTANTS, assistants_table
from chat.language_model import GPT, LLM, OLLAMA

app = typer.Typer(help="Cli to interact with OpenAI chat models")

assistants_enum = enum.Enum("Roles", dict([(d, d) for d in ASSISTANTS.keys()]))


def get_model(lm):
    if lm == LLM.GPT4:
        if not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
            print("OPENAI_API_KEY not set!")
            exit()
        GPT()

    elif lm == LLM.DOLPHIN_MIXTRAL:
        OLLAMA(lm)
    return OLLAMA()


@app.command(name="chat", help="Start chat session.")
def chat_command(
    assistant: assistants_enum = typer.Argument(
        default="default", help="Assistant profile to be used."
    ),
    lm: LLM = typer.Option(default=LLM.DOLPHIN_MISTRAL, help="lm to be used"),
):
    Chat(ASSISTANTS[assistant.value], get_model(lm)).start()


@app.command(name="assistants", help="List all available assisent profiles")
def assistants():
    print(assistants_table())


if __name__ == "__main__":
    app()
