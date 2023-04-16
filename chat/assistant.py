import subprocess

from rich.table import Table

ASSISTANTS = {}


class Assistant:
    def __init__(self, icon, help, prompt):
        self.icon = icon
        self._prompt = prompt
        self.help = help

    def prompt(self):
        if callable(self._prompt):
            content = self._prompt()
        else:
            content = self._prompt
        return {"role": "system", "content": content}

    def banner(self):
        return f"{self.icon} {self.help}"


ASSISTANTS["default"] = Assistant(
    "🤖",
    "The vanilla assistant",
    "You are a helpful assistant who communicates directly and succintly. Use markdown for formatting",
)


ASSISTANTS["unhelpful"] = Assistant(
    "🤪",
    "The unhelpfull assistant",
    "You are a unhelpful assistant who adds mostly unrelated information",
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
            readme = run_bash(f"cat {file}")
            break
    return f"You're are the assisent of a developer for a specific repository. This is the Readme:{readme}. This is the output of git status: {git_status}, This is the current git diff: {git_diff}"


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
