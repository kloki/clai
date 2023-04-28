from .base import ASSISTANTS, Assistant
from .utils import run_bash

ASSISTANTS["test_data"] = Assistant(
    "🧪 ",
    "The dummy test data assistant",
    [
        "You are a helpful assistant who dummy data for a developer or tester",
        "Please provide data in json that is formatted to be readable. Keys should be in snake_case",
        "Always give 3 or more examples.",
    ],
)


def language_assistant(name, icon):
    ASSISTANTS[name] = Assistant(
        icon,
        f"The {name} assistant",
        [
            f"You are a helpful assistant helping a developer learn the programming language {name}. Provide examples with your answers",
        ],
    )


language_assistant("rust", "🦀")
language_assistant("python3", "🐍")
language_assistant("go", "🐹 ")


def git_prompt():
    git_status = run_bash("git status")
    git_diff = run_bash("git diff")
    files = run_bash("ls").split("\n")
    readme = ""
    for file in files:
        if "readme" in file.lower():
            with open(file, "r") as infile:
                readme = infile.read()
            break

    messages = [
        {
            "role": "system",
            "content": "You're are the assisent of a developer for a specific repository.",
        }
    ]
    if readme:
        messages.append(
            {"role": "user", "content": f"This is the readme:\n```{readme}```"}
        )

    messages.append(
        {
            "role": "user",
            "content": f"This is the ouput of `git status`:\n```{git_status}```",
        }
    )
    messages.append(
        {
            "role": "user",
            "content": f"This is the ouput of `git diff`:\n```{git_diff}```",
        }
    )
    return messages


ASSISTANTS["git"] = Assistant(
    "👷",
    "The git assistant",
    git_prompt,
)


ASSISTANTS["bash"] = Assistant(
    "🖥️ ",
    "The bash assistant",
    [
        "You are a helpful assistant helping a developer using the unix cli. You will provide help with bash and unix commands"
    ],
)
