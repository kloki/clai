import asyncio
import time

from textual import on
from textual.app import App, Widget
from textual.reactive import reactive
from textual.widgets import Input, Label

from .assistant import ASSISTANTS
from .language_model import OLLAMA
from .session import Session


class Question(Label):
    pass


class Answer(Label):
    content = reactive("content", layout=True)

    def render(self) -> str:
        return self.content


class ChatBox(Widget):

    def add_question(self, question):

        self.mount(Question(question))
        self.scroll_down()

    def create_answer(self, content):
        answer = Answer(content)
        self.mount(Answer(content))
        self.scroll_down()
        return answer


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
        answer = chatbox.create_answer("...")

        async def response_task():
            for t in ["asht", "asthwasht", "ash", "ashtashttht"]:
                time.sleep(1)
                answer.update(t)

        asyncio.create_task(response_task())
        input.value = ""
