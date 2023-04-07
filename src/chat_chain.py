from typing import Dict, List

from langchain.chains.llm import LLMChain
from langchain.schema import BaseRetriever
from langchain.chat_models.base import BaseChatModel
from langchain.memory.chat_memory import BaseChatMemory
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.callbacks.base import BaseCallbackManager


class ChatChain(LLMChain):
    """Chain to use to answer questions in a chat."""
    retriever: BaseRetriever
    combine_docs_chain: BaseCombineDocumentsChain
    llm: BaseChatModel
    memory: BaseChatMemory
    question_generator: LLMChain
    callback_manager: BaseCallbackManager

    input_key = "question"
    output_key = "answer"

    @property
    def input_keys(self) -> List[str]:
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        question = inputs["question"].strip()
        history = inputs["history"]
        if history:
            new_question = self.question_generator.run(
                question=question, chat_history=history
            )
        else:
            new_question = question

        docs = self.retriever.get_relevant_documents(new_question)
        doc_template = """
        Doc: {title}
        Url: {url}
        Content: {content}
        """
        context = "\n".join([
            doc_template.format(title=doc.metadata.get("title"),
                                url=doc.metadata.get("source"),
                                content=doc.page_content) for doc in docs
        ])
        # context, _ = self.combine_docs_chain.combine_docs(docs, question=new_question)

        inputs = dict(context=context, question=new_question)
        prompts, _ = self.prep_prompts([inputs])
        messages = prompts[0].to_messages()
        user_message = messages.pop(-1)
        complete_dialog = [*messages,
                           *history,
                           user_message
                           ]
        answer = self.llm(complete_dialog)
        outputs = {self.output_key: answer.content}

        return outputs

    async def _acall(self, inputs: Dict[str, str]) -> Dict[str, str]:
        raise NotImplementedError
