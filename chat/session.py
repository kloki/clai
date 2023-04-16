class Session:
    def __init__(self, role):
        self.role = role
        self.messages = role.introduction()

    def question(self, question):
        self.messages.append({"role": "user", "content": question})

    def answer(self, answer):
        self.messages.append({"role": "assistant", "content": answer})

    def payload(self):
        return self.messages

    def new_message(self):
        return self.messages[-1]["content"]

    def money_spend(self):
        total = 0
        total_sum = 0
        for m in self.messages:
            total_sum += len(m["content"])
            if m["role"] == "user":
                total += total_sum

        return round(((total / 4000) * 0.002), 3)
