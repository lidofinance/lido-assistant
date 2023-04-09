from langchain.prompts import BaseChatPromptTemplate
from typing import List
from langchain.agents import Tool
from langchain.schema import HumanMessage

template = """Answer the following questions as best as you can. You have access to the following tools:

{tools}

Do not include information not explicitly asked for. Answer the question that the user asked, with no additional information.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Action: another action to take, should be one of [{tool_names}]
Action Input: the input to the action
...

Observations: the result of the actions
... (this Thought/Actions/Action Inputs/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Do not include Observations until you have listed all the actions you want to take. If the tool provides a source URL, include it in your final answer.
Actions and Action Inputs should always come in pairs. If you want to use a tool, you must provide an input to it.

Do not provide a response outside of the format above. If you do not know how to answer a question, your final answer should be "I don't know".

Begin!

Question: {input}
{agent_scratchpad}"""


class CustomPromptTemplate(BaseChatPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservations: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]


def get_prompt_template(tools: List[Tool]):
    return CustomPromptTemplate(template=template, tools=tools, input_variables=["input", "intermediate_steps"])
