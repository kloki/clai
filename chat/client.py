import json
import uuid

import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter, WordCompleter, merge_completers
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.padding import Padding
from rich.prompt import Prompt
from rich.spinner import Spinner

from .assistant import ASSISTANTS, assistants_table
from .session import Session


class Client:
    def __init__(self, assistant=None):
        self.assistant = assistant if assistant else ASSISTANTS["default"]
        self.session = Session(self.assistant)
        self.console = Console()
        self.language_model = "gpt-3.5-turbo"

        self.commands = {
            "\quit": self.exit,
            "\q": self.exit,
            "\exit": self.exit,
            "\dump": self.dump,
            "\switch": self.switch,
            "\clear": self.clear,
            "\load": self.load,
            "\help": self.help,
        }

        self.prompt = PromptSession(
            completer=merge_completers(
                [PathCompleter(), WordCompleter(self.commands.keys(), sentence=True)]
            )
        )

    def system_message(self, message):
        self.console.print(f"[cyan]💡 {message}")

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
        self.system_message(f"Chat started assistant: {self.assistant.banner()}")
        while True:
            question = self.ask_user()
            if not self.system_command(question):
                self.ask_assistent(question)
                self.print_answer()

    def print_answer(self):
        self.console.print(
            f"\n<<< {self.assistant.icon} [green] \[~${self.session.money_spend()}]"
        )
        self.console.print(Padding(Markdown(self.session.new_message()), (0, 4)))
        self.console.print("")

    def query_model(self, question):
        self.session.question(question)
        response = openai.ChatCompletion.create(
            model=self.language_model, messages=self.session.payload()
        )
        self.session.answer(response["choices"][0]["message"]["content"])

    # Chat commands
    def exit(self, question):
        self.system_message("Exiting....")
        exit()

    def help(self, question):
        self.system_message(
            "Possible commands \n  - " + "\n  - ".join(self.commands.keys())
        )

    def clear(self, question):
        self.system_message("Clearing session.")
        self.clear_session()

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
        self.session.question(
            f"This it the content of the file `{file}`: ```{content}```"
        )
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

    def system_command(self, question):
        if question[0] not in ["\\", "/", "."]:
            return False

        if question[0] in ["/", "."]:
            question = "\load " + question
        command = question.split(" ")[0]

        if command not in self.commands:
            self.system_message("Unknow command!")
            return True
        self.commands[command](question)
        return True
