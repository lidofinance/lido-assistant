from src.chat_agent import get_agent

agent = get_agent()

res = agent.run("What does Lido do? What is the current price of LDO in USD?")
print(res)
