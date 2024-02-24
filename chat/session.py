import json
from uuid import uuid4


class Session:
    def __init__(self, role):
        self.role = role
        self.base = role.instructions()
        self.messages = []

    def question(self, question):
        self.messages.append({"role": "user", "content": question})

    def answer(self, answer):
        self.messages.append({"role": "assistant", "content": answer})

    def payload(self):
        return self.base + self.messages

    def reset(self):
        self.messages = []

    def dump(self):
        name = f"{uuid4()}.json"
        with open(name, "w", encoding="utf-8") as f:
            json.dump(self.payload(), f, ensure_ascii=False, indent=4)
        return name
