import json
import uuid

import openai
from prompt_toolkit import PromptSession
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
        self.prompt = PromptSession()
        self.language_model = "gpt-3.5-turbo"

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

    def clear_session(self):
        self.session = Session(self.assistant)

    def system_command(self, question):
        if not question.startswith("/"):
            return False
        question = question[1:].lower()

        if question in ["quit", "bye", "exit"]:
            self.system_message("Exiting...")
            exit()
        elif "clear" in question:
            self.system_message("Clearing session.")
            self.clear_session()

        elif "dump" in question:
            guid = str(uuid.uuid4())
            self.system_message(f"Dumping session to {guid}.json")
            self.dump_session(guid)

        elif "switch" in question:
            self.system_message("Choose assissent")
            self.console.print(assistants_table())
            assistant_id = Prompt.ask(
                choices=ASSISTANTS.keys(),
                default="default",
            )
            self.system_message(f"Switching to {assistant_id}")
            self.assistant = ASSISTANTS[assistant_id]
            self.clear_session()

        else:
            self.system_message("Unkown command.")
        return True

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

    def query_model(self, question):
        self.session.question(question)
        response = openai.ChatCompletion.create(
            model=self.language_model, messages=self.session.payload()
        )
        self.session.answer(response["choices"][0]["message"]["content"])
