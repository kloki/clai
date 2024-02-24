import asyncio
import time

from textual import on, work
from textual.app import App, Widget
from textual.reactive import reactive
from textual.widgets import Input, Label

from .assistant import ASSISTANTS
from .language_model import OLLAMA
from .session import Session


class Question(Label):
    pass


class Answer(Label):

    pass


class ChatBox(Widget):

    def add_question(self, question):

        self.mount(Question(question))
        self.scroll_down()

    def create_answer(self, content):
        self.mount(Answer(content))
        self.scroll_down()

    def update_answer(self, content):
        answer = self.query(Answer).last()
        answer.update(content)
        self.scroll_down()


class StatusBar(Label):
    pass


class Client(App):
    CSS_PATH = "style.css"

    def __init__(self, assistant=None, model=OLLAMA()):
        super().__init__()
        self.assistant = assistant if assistant else ASSISTANTS["default"]
        self.session = Session(self.assistant)
        self.model = model

    def compose(self):
        yield ChatBox()
        yield Input(type="text", placeholder="Ask a question.")
        yield StatusBar(
            f"{self.assistant.banner()} - {self.model.icon} {self.model.name}"
        )

    @on(Input.Submitted)
    def proces_question(self):
        input = self.query_one(Input)
        question = input.value
        if question == "":
            return

        chatbox = self.query_one(ChatBox)
        chatbox.add_question(question)
        chatbox.create_answer("...")

        input.clear()
        input.disabled = True
        self.fetch_answer()

    @work(exclusive=True)
    async def fetch_answer(self) -> None:
        chatbox = self.query_one(ChatBox)

        for t in ["asht", "ashtasht", "asht", "done\n\n\n\n\n\n"]:
            chatbox.update_answer(t)
        input = self.query_one(Input)
        input.disabled = False
        input.focus()
