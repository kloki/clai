class ChatGPT3:
    name = "gpt-3.5-turbo"
    price_per_token = 0.000002

    def money_spend(self, tokens):
        return round(tokens * self.price_per_token, 3)
