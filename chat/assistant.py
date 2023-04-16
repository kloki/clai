import subprocess

from rich.table import Table

ASSISTANTS = {}


class Assistant:
    def __init__(self, icon, help, context):
        self.icon = icon
        self.context = context
        self.help = help

    def instructions(self):
        if callable(self.context):
            return self.context()
        messages = [{"role": "user", "content": c} for c in self.context]
        messages[0]["role"] = "system"
        return messages

    def banner(self):
        return f"{self.icon} {self.help}"


ASSISTANTS["default"] = Assistant(
    "🤖",
    "The vanilla assistant",
    [
        "You are a helpful assistant who communicates directly and succintly."
        "Use markdown for formatting."
    ],
)


ASSISTANTS["unhelpful"] = Assistant(
    "🤪",
    "The unhelpfull assistant",
    [
        "You are a unhelpful assistant who adds mostly unrelated information",
        "Avoid punctuation.",
    ],
)

ASSISTANTS["cook"] = Assistant(
    "🍛",
    "The (vegetarian) cooking assistant",
    [
        "You are a helpful assistant who provides recipes and suggestions for cooking.",
        "Only suggest vegetarian recipes.",
        "Use markdown for formatting.",
        "Use metric weight measurements.",
        "Don't use volumetric measurements.",
    ],
)


def run_bash(command):
    return (
        subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
        .stdout.read()
        .decode("utf-8")
    )


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


def assistants_table():
    table = Table("id", "icon", "description")
    for k, v in ASSISTANTS.items():
        table.add_row(k, v.icon, v.help)
    return table
