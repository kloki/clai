import enum
import os
import subprocess

import typer
from rich import print

from chat import Chat
from chat.assistant import ASSISTANTS, assistants_table

app = typer.Typer(help="Cli to interact with OpenAI chat models")

assistants_enum = enum.Enum("Roles", dict([(d, d) for d in ASSISTANTS.keys()]))


@app.command(name="chat", help="Start chat session.")
def chat_command(
    assistant: assistants_enum = typer.Argument(
        default="default", help="Assistant profile to be used."
    )
):
    Chat(ASSISTANTS[assistant.value]).start()


@app.command(name="assistants", help="List all available assisent profiles")
def assistants():
    print(assistants_table())


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
        print("OPENAI_API_KEY not set!")
    app()
