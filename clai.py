#!/usr/bin/env python3

import os

import click

from chat import Client
from chat.assistant import ASSISTANTS
from chat.language_model import Dummy, Ollama, OpenAI


def get_model(lm):
    if lm == "gpt":
        if not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
            print("OPENAI_API_KEY not set!")
            exit()
        return OpenAI()

    if lm == "dummy":
        return Dummy()
    if lm == "dolphin_+":
        return Ollama("dolphin-mixtral")
    return Ollama()


@click.command()
@click.option(
    "-l",
    "--llm",
    type=click.Choice(["dummy", "dolphin", "dolpin+", "gpt"]),
    default="dummy",
)
@click.option(
    "-a", "--assistant", type=click.Choice(list(ASSISTANTS.keys())), default="default"
)
def app(
    llm,
    assistant,
):
    model = get_model(llm)
    assistant = ASSISTANTS[assistant]
    tui = Client(model, assistant)
    tui.run()


if __name__ == "__main__":
    app()
