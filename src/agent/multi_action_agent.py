from langchain import LLMChain
from typing import List, Tuple, Any, Union
from langchain.agents import AgentOutputParser, BaseMultiActionAgent
from langchain.schema import AgentAction, AgentFinish


class MultiActionAgent(BaseMultiActionAgent):

    llm_chain: LLMChain
    output_parser: AgentOutputParser
    stop: List[str]

    @property
    def input_keys(self) -> List[str]:
        return list(set(self.llm_chain.input_keys) - {"intermediate_steps"})

    def plan(self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any) -> Union[List[AgentAction], AgentFinish]:
        print("Calling LLM")
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool(s) to use.
        """
        output = self.llm_chain.run(
            intermediate_steps=intermediate_steps, stop=self.stop, **kwargs
        )

        # Return the parsed output
        return self.output_parser.parse(output)

    def aplan(self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any) -> Union[List[AgentAction], AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool(s) to use.
        """
        output = self.llm_chain.run(
            intermediate_steps=intermediate_steps, stop=self.stop, **kwargs
        )

        # Return the parsed output
        return self.output_parser.parse(output)
