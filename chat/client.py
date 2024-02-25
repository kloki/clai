import pyperclip
from rich.markdown import Markdown
from textual import on, work
from textual.app import App, Widget
from textual.events import Click
from textual.widgets import Input, Label

from .assistant import ASSISTANTS
from .language_model import Ollama, get_next_llm
from .session import Session


class ChatItem(Label):

    @on(Click)
    async def on_click(self, event: Click) -> None:
        pyperclip.copy(self.renderable.markup)
        self.styles.animate("opacity", 0.5, duration=0.1)
        self.styles.animate("opacity", 1.0, duration=0.1, delay=0.1)


class UserLabel(Label):
    pass


class ChatBox(Widget):

    def on_mount(self):
        self.mount(Label())

    @staticmethod
    def md(content):
        return Markdown(content, code_theme="dracula")

    def add_question(self, question):

        self.mount(Label("You", classes="chatlabel user"))
        self.mount(ChatItem(self.md(question)))
        self.scroll_end()

    def create_answer(self, name, content):
        self.mount(Label(name, classes="chatlabel llm"))
        self.mount(ChatItem(self.md(content)))
        self.scroll_end()

    def update_answer(self, content):
        answer = self.query(ChatItem).last()
        answer.update(self.md(content))
        self.scroll_end()

    def reset(self):
        self.remove_children()
        self.mount(Label())


class StatusBar(Label):

    pass


class Client(App):
    CSS_PATH = "style.css"
    BINDINGS = [
        ("ctrl+x", "quit", "Quit"),
        ("ctrl+c", "clear_session()", "Clear"),
        ("ctrl+j", "dump_session()", "Dump"),
        ("ctrl+t", "toggle_llm()", "Toggle llm"),
    ]

    def __init__(self, model=Ollama(), assistant=None):
        super().__init__()
        self.assistant = assistant if assistant else ASSISTANTS["default"]
        self.session = Session(self.assistant)
        self.model = model

    def compose(self):
        yield ChatBox()
        yield Input(type="text", placeholder="Ask a question.")
        yield Label(self.status_bar_content(), classes="statusbar")

    def status_bar_content(self):
        return f"{self.assistant.banner()} - {self.model.icon}  {self.model.name}"

    def action_clear_session(self):
        self.session.reset()
        self.query_one(ChatBox).reset()
        self.notify("Cleared")

    def action_dump_session(self):
        name = self.session.dump()
        self.notify(f"Dumped session to: {name}")

    def action_toggle_llm(self):
        self.model = get_next_llm(self.model)
        self.query_one(".statusbar").update(self.status_bar_content())
        self.notify(f"Toggled to {self.model.icon} {self.model.name}")

    @on(Input.Submitted)
    def proces_question(self):
        input = self.query_one(Input)
        question = input.value
        if question == "":
            return

        chatbox = self.query_one(ChatBox)
        chatbox.add_question(question)
        self.session.question(question)
        chatbox.create_answer(self.assistant.icon, "...")

        input.clear()
        input.disabled = True
        input.placeholder = "Processing..."
        self.fetch_answer()

    @work(exclusive=True)
    async def fetch_answer(self) -> None:
        chatbox = self.query_one(ChatBox)

        result = ""
        async for chunk in self.model.query(self.session):
            result += chunk
            chatbox.update_answer(result)
        self.session.answer(result)
        input = self.query_one(Input)
        input.disabled = False
        input.placeholder = "Ask a question."
        input.focus()

    def key_space(self) -> None:
        self.bell()
