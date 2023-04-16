import os

from chat import Chat
from chat.role import DEFAULT

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
        print("OPENAI_API_KEY not set!")
    chat = Chat(DEFAULT)
    chat.start()
