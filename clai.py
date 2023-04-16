import os

from chat import Chat

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
        print("OPENAI_API_KEY not set!")
    chat = Chat()
    chat.start()
