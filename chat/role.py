from rich.table import Table

ROLES = {}


class Role:
    def __init__(self, icon, help, prompt):
        self.icon = icon
        self._prompt = prompt
        self.help = help

    def prompt(self):
        return {"role": "system", "content": self._prompt}

    def banner(self):
        return f"{self.icon} {self.help}"


ROLES["default"] = Role(
    "🤖",
    "The vanilla assistant",
    "You are a helpful assistant who communicates directly and succintly. Use markdown for formatting",
)

ROLES["unhelpful"] = Role(
    "🤪",
    "The unhelpfull assistant",
    "You are a unhelpful assistant who adds mostly unrelated information",
)


def roles_table():
    table = Table("id", "icon", "description")
    for k, v in ROLES.items():
        table.add_row(k, v.icon, v.help)
    return table
