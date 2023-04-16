import openai
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.spinner import Spinner

from .session import Session


class Client:
    def __init__(self, role):
        self.role = role
        self.session = Session(role)
        self.console = Console()
        self.leave_command = ["bye", "exit"]

    def start(self):
        self.console.print("Chat Started")
        while True:
            question = input(">>> ")
            if question.lower() in self.leave_command:
                exit()
            with Live(
                Spinner("dots12", style="green"), refresh_per_second=20, transient=True
            ):
                self.ask_question(question)
            self.console.print("<<<")
            self.console.print(Markdown(self.session.new_message()))

    def ask_question(self, question):
        self.session.question(question)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.session.payload()
        )
        self.session.answer(response["choices"][0]["message"]["content"])
