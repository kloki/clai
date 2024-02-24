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
