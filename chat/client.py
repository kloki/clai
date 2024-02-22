from textual.app import App

from . import colors
from .assistant import ASSISTANTS
from .language_model import OLLAMA
from .session import Session


class Client(App):
    def __init__(self, assistant=None, model=OLLAMA()):
        super().__init__()
        self.assistant = assistant if assistant else ASSISTANTS["default"]
        self.session = Session(self.assistant)
        self.model = model

    def on_mount(self):
        self.screen.styles.background = colors.background
