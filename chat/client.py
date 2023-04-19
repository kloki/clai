import json
import uuid

import openai
import pyperclip
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter, WordCompleter, merge_completers
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.padding import Padding
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.table import Table

from .assistant import ASSISTANTS, assistants_table
from .language_model import GPT3
from .session import Session


class Client:
    def __init__(self, assistant=None, model=GPT3()):
        self.assistant = assistant if assistant else ASSISTANTS["default"]
        self.session = Session(self.assistant)
        self.console = Console()
        self.model = model
        self.inserted_files = []
        self.tokens = 0

        self.commands = {
            "\quit": self.exit,
            "\q": self.exit,
            "\exit": self.exit,
            "\dump": self.dump,
            "\switch": self.switch,
            "\clear": self.clear,
            "\load": self.load,
            "\help": self.help,
            "\clip": self.copy_to_clipboard,
            "\\assistant_instructions": self.instructions,
        }

        self.commands = {
            "\q": (self.exit, "Exit the program"),
            "\c": (
                self.copy_to_clipboard,
                "Copy the last response to the clipboard",
            ),
            "\dump": (self.dump, "Dump the current chat thread to a file"),
            "\switch": (self.switch, "Switch to a different assistatn"),
            "\clear": (self.clear, "Clear the current chat thread"),
            "\load": (
                self.load,
                "Load a file and add it to the context of the assistant",
            ),
            "\help": (self.help, "Display this help message"),
            "\\assistant_instructions": (
                self.instructions,
                "List the instruction of the current assistant",
            ),
        }
        self.prompt = PromptSession(
            completer=merge_completers(
                [PathCompleter(), WordCompleter(self.commands.keys(), sentence=True)]
            )
        )

    def system_message(self, message, data=None):
        self.console.print(f"[cyan]💡 {message}")
        if data:
            self.console.print(Padding(Markdown(data), (0, 4)))

    def ask_user(self):
        return self.prompt.prompt(">>> ")

    def dump_session(self, name):
        with open(f"{name}.json", "w") as outfile:
            json.dump(self.session.messages, outfile)

    def ask_assistent(self, question):
        with Live(
            Spinner("dots12", style="green"), refresh_per_second=20, transient=True
        ):
            self.query_model(question)

    def start(self):
        self.system_message(
            f"Chat: {self.assistant.banner()} [green]🧠 {self.model.name}"
        )
        while True:
            question = self.ask_user()
            if not self.system_command(question):
                self.ask_assistent(question)
                self.print_answer()

    def print_answer(self):
        self.console.print(
            f"\n<<< {self.assistant.icon} [green] \[${self.model.money_spend(self.tokens)}]"
        )
        self.console.print(Padding(Markdown(self.session.new_message()), (0, 4)))
        self.console.print("")

    def query_model(self, question):
        self.session.question(question)
        response = openai.ChatCompletion.create(
            messages=self.session.payload(), **self.model.settings()
        )
        self.session.answer(response["choices"][0]["message"]["content"])
        self.tokens += response["usage"]["total_tokens"]

    # Chat commands
    def exit(self, question):
        self.system_message("Exiting....")
        exit()

    def help(self, question):
        table = Table("command", "description")
        for k, v in self.commands.items():
            table.add_row(k, v[1])
        self.system_message("System commands")
        self.console.print(Padding(table, (0, 4)))

    def instructions(self, question):
        data = "\n".join([f"- {m['content']}" for m in self.assistant.instructions()])
        self.system_message("Assistant instructions:", data=data)
        if self.inserted_files:
            data = "\n".join([f"- {f}" for f in self.inserted_files])

            self.system_message("Loaded Files:", data=data)

    def clear(self, question):
        self.system_message("Clearing session.")
        self.clear_session()
        self.inserted_files = []
        self.tokens = 0

    def dump(self, question):
        guid = str(uuid.uuid4())
        self.system_message(f"Dumping session to {guid}.json")
        self.dump_session(guid)

    def load(self, question):
        content = ""
        file = ""
        try:
            file = question.split(" ")[1]
            with open(file, "r") as infile:
                content = infile.read()
        except (IndexError, IsADirectoryError, FileNotFoundError):
            self.system_message("Invalid File")
            return
        if not content:
            self.system_message("Invalid File")
            return
        payload = f"This it the content of the file `{file}`:\n ```{content}```"
        self.session.question(payload)
        self.inserted_files.append(payload)
        self.system_message(f"Added {file} to context of assistant.")

    def clear_session(self):
        self.session = Session(self.assistant)

    def switch(self, question):
        items = question.split(" ")
        if len(items) > 1 and items[1] in ASSISTANTS.keys():
            assistant_id = items[1]
        else:
            self.system_message("Choose assistent")
            self.console.print(Padding(assistants_table(), (0, 4)))
            assistant_id = Prompt.ask(
                choices=ASSISTANTS.keys(),
                default="default",
            )
        self.system_message(f"Switching to {assistant_id}")
        self.assistant = ASSISTANTS[assistant_id]
        self.clear_session()

    def copy_to_clipboard(self, question):
        content = self.session.messages[-1]["content"]
        if "```" in content:
            content = content.split("```")[1]
            self.system_message("Copied text block in last response to clipboard")
        else:
            self.system_message("Copied last response to clipboard")

        pyperclip.copy(content)

    def system_command(self, question):
        if question[0] not in ["\\", "/", "."]:
            return False

        if question[0] in ["/", "."]:
            question = "\load " + question
        command = question.split(" ")[0]

        if command not in self.commands:
            self.system_message("Unknow command!")
            command = "\help"
        self.commands[command][0](question)
        return True
