#!/usr/bin/env python3

import os

import click

from chat import Client
from chat.assistant import ASSISTANTS
from chat.language_model import LLM


def get_model(lm):
    if lm == "gpt":
        if not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
            print("OPENAI_API_KEY not set!")
            exit()
    return LLM[lm]


@click.command()
@click.option(
    "-l",
    "--llm",
    type=click.Choice(list(LLM.keys())),
    default="dolphin",
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
