from langchain.utilities import TextRequestsWrapper
from langchain import SerpAPIWrapper
from langchain.agents import Tool
from src.chat_model import chat


def get_tools():
    requests = TextRequestsWrapper()

    def coinGeckoSearch(_):
        res = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids=lido-dao&vs_currencies=usd"
        )
        return res

    def defiLlamaTVL(_):
        res = requests.get(
            f"https://api.llama.fi/tvl/lido"
        )
        return res

    tools = [
        Tool(
            name="Lido Documentation QA System",
            func=chat().run,
            description="useful for when you need to answer questions about Lido. Input should be a fully formed question.",
        ),
        Tool(
            name="Price Feed",
            func=coinGeckoSearch,
            description="useful for when you need to answer questions about the price of Lido DAO token. Returns the current price of Lido DAO token in USD. Source: CoinGecko"
        ),
        Tool(
            name="TVL",
            func=defiLlamaTVL,
            description="returns the Total Value Locked (TVL) of Lido. Source: DefiLlama"
        )
    ]

    return tools
