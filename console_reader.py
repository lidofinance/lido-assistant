from src.chat_model import chat


def run():
    qa = chat()
    while True:
        q = input('Question: ')
        if q == 'done':
            break
        print("AI: " + qa({"question": q})["answer"])
