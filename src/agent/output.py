from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
from typing import List, Union
import re


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[List[AgentAction], AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split(
                    "Final Answer:")[-1].strip()},
                log=llm_output,
            )

        def extract_actions_and_inputs(text):
            actions = re.findall(r'Action: (.+)', text)
            action_inputs = re.findall(r'Action Input: (.+)', text)

            return actions, action_inputs

        # Parse the actions and action inputs out of the llm_output string and thne return a list of AgentActions for each parsed action and action input
        # You can use the following regex to parse out the actions and action inputs:
        actions, action_inputs = extract_actions_and_inputs(llm_output)
        agent_actions = []
        if (len(actions) != len(action_inputs)):
            raise ValueError(
                f"Could not parse LLM output: `{llm_output}`. Number of actions and action inputs do not match.")
        for action, action_input in zip(actions, action_inputs):
            print(action, action_input)
            agent_actions.append(AgentAction(
                tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output))
        return agent_actions
