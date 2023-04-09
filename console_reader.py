from src.chat_model import chat
from src.chat_agent import get_agent


def run():
    agent = get_agent()
    while True:
        q = input("Question: ")
        if q == "done":
            break
        print("AI: " + agent.run(q))
