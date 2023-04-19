#!/usr/bin/env python3
import enum
import os

import typer
from rich import print

from chat import Chat
from chat.assistant import ASSISTANTS, assistants_table
from chat.language_model import GPT3

app = typer.Typer(help="Cli to interact with OpenAI chat models")

assistants_enum = enum.Enum("Roles", dict([(d, d) for d in ASSISTANTS.keys()]))


@app.command(name="chat", help="Start chat session.")
def chat_command(
    assistant: assistants_enum = typer.Argument(
        default="default", help="Assistant profile to be used."
    ),
    temperature: int = typer.Option(default=1, help="Temperature used by model"),
    top_p: int = typer.Option(default=1, help="Top_p used by model"),
):
    Chat(ASSISTANTS[assistant.value], GPT3(temperature, top_p)).start()


@app.command(name="assistants", help="List all available assisent profiles")
def assistants():
    print(assistants_table())


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
        print("OPENAI_API_KEY not set!")
        exit()
    app()
