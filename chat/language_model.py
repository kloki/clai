from enum import Enum


class LanguageModel(str, Enum):
    GPT3 = "gpt3"
    GPT4 = "gpt4"


class GPT3:
    name = "gpt-3.5-turbo-16k-0613"
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


class GPT4:
    name = "gpt-4"
    price_per_token = 0.00006

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


def get_model(lm):
    if lm == LanguageModel.GPT4:
        return GPT4
    return GPT3
