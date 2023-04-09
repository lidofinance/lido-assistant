from src.agent.multi_action_agent import MultiActionAgent
from src.agent.output import CustomOutputParser
from src.agent.prompts import get_prompt_template
from src.agent.tools import get_tools
from langchain.agents import AgentExecutor

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI


def get_agent():

    tools = get_tools()

    llm = ChatOpenAI(temperature=0)
    llm_chain = LLMChain(llm=llm, prompt=get_prompt_template(tools))
    output_parser = CustomOutputParser()
    agent = MultiActionAgent(llm_chain=llm_chain,
                             output_parser=output_parser, stop=["Observation:", "Observations:"])

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True)

    return agent_executor
