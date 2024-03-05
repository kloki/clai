from rich.table import Table

ASSISTANTS = {}


class Assistant:
    def __init__(self, icon, help, context):
        self.icon = icon
        self.context = context
        self.help = help

    def instructions(self):
        return [{"role": "system", "content": self.context}]

    def banner(self):
        return f"{self.icon} {self.help}"


def assistants_table():
    table = Table("id", "icon", "description")
    for k, v in ASSISTANTS.items():
        table.add_row(k, v.icon, v.help)
    return table


ASSISTANTS["default"] = Assistant(
    "🤖",
    "The vanilla assistant",
    "You are a helpful assistant who communicates directly and succintly."
    "Use markdown for formatting.",
)
