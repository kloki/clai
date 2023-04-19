class GPT3:
    name = "gpt-3.5-turbo"
    price_per_token = 0.000002

    def __init__(self, temperature=1, top_p=1):
        self.temperature = temperature
        self.top_p = top_p

    def money_spend(self, tokens):
        return round(tokens * self.price_per_token, 3)

    def settings(self):
        return {
            "model": self.name,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }
