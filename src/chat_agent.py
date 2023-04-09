from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import LLMChain
from langchain.utilities import TextRequestsWrapper
from langchain.memory import ConversationBufferMemory
from src.chat_model import chat
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI


def get_agent():
    requests = TextRequestsWrapper()

    llm = ChatOpenAI(temperature=0)

    def coinGeckoSearch(_):
        res = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids=lido-dao&vs_currencies=usd"
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
            description="useful for when you need to answer questions about the price of Lido DAO token. Returns the current price of Lido DAO token in USD."
        )
    ]

    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)

    LIDO_HUMAN_MSG = """TOOLS
------
Assistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:

{{tools}}

{format_instructions}

If a tool provides a source, include the source in your final answer. Do not overly paraphrase the tool's output if it answers the question with sufficient clarity.

USER'S INPUT
--------------------
Here is the user's input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else). You should never return more than one action at once:

{{{{input}}}}"""

    agent_chain = initialize_agent(
        tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory, agent_kwargs={"human_message": LIDO_HUMAN_MSG})

    return agent_chain
