from typing import Any, Union, Dict

from langchain.schema import LLMResult, AgentFinish, AgentAction
from langchain.callbacks.base import BaseCallbackHandler

from src.loaders import replace_aliases_with_addresses, replace_addresses_with_aliases


class AddressesCallbackManager(BaseCallbackHandler):

    def __init__(self, addresses):
        self.addresses = addresses
        super().__init__()

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        pass

    def on_llm_start(self, response: LLMResult, **kwargs):
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        pass

    def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        pass

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> Any:
        inputs["question"] = replace_addresses_with_aliases(inputs["question"], self.addresses)
        for message in inputs["history"]:
            message.content = replace_addresses_with_aliases(message.content, self.addresses)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        outputs["answer"] = replace_aliases_with_addresses(outputs["answer"], self.addresses)

    def on_chain_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        pass

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        pass

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        pass

    def on_tool_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        pass

    def on_text(self, text: str, **kwargs: Any) -> Any:
        pass

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        pass

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        pass
