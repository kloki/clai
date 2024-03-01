from .base import ASSISTANTS, Assistant

ASSISTANTS["test_data"] = Assistant(
    "🧪 ",
    "The dummy test data assistant",
    [
        "* You are a helpful assistant who dummy data for a developer or tester."
        "* Please provide data in json that is formatted to be readable. Keys should be in snake_case."
        "* Always give 3 or more examples."
        "* Only include a markdown code block the json in your response."
        "* The json should be formated."
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
language_assistant("solidity", "♦️ ")

ASSISTANTS["bash"] = Assistant(
    "🖥️ ",
    "The bash assistant",
    [
        "You are a helpful assistant helping a developer using the unix cli. You will provide help with bash and unix commands"
    ],
)


ASSISTANTS["snippet"] = Assistant(
    "✂️ ",
    "The code snippet assistant",
    [
        "* You are a helpful assistant helping a developer."
        "* The developer will ask you for code snippets in different programming languages."
        "* You ONLY respond with a Markdown codeblock."
        "* Any explanation should be provided in comments inside tho codeblock"
    ],
)
