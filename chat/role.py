class Role:
    def __init__(self, prompt):
        self._prompt = prompt

    def prompt(self):
        return {"role": "system", "content": self._prompt}


DEFAULT = Role("You are a helpful assistant.")
