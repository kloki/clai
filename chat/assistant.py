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


def assistants_table():
    table = Table("id", "icon", "description")
    for k, v in ASSISTANTS.items():
        table.add_row(k, v.icon, v.help)
    return table
