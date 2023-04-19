class Session:
    def __init__(self, role):
        self.role = role
        self.messages = role.instructions()

    def question(self, question):
        self.messages.append({"role": "user", "content": question})

    def answer(self, answer):
        self.messages.append({"role": "assistant", "content": answer})

    def payload(self):
        return self.messages

    def new_message(self):
        return self.messages[-1]["content"]
