from langchain import OpenAI, LLMChain
from langchain.callbacks import CallbackManager
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks.stdout import StdOutCallbackHandler

from src.database import get_database
from src.chat_chain import ChatChain
from src.callback_managers import AddressesCallbackManager
from src.prompts import qa_prompt


def chat():
    db, addresses = get_database()
    doc_chain = load_qa_chain(
        chain_type="map_reduce",
        llm=OpenAI(
            temperature=0,
            verbose=True,
        ),
    )
    condense_question_chain = LLMChain(llm=OpenAI(
        temperature=0, verbose=False,
    ), prompt=CONDENSE_QUESTION_PROMPT)
    model = ChatChain(
        combine_docs_chain=doc_chain,
        question_generator=condense_question_chain,
        retriever=db.as_retriever(search_type="mmr"),
        llm=ChatOpenAI(
            temperature=0.01,
            verbose=True,
        ),
        memory=ConversationBufferWindowMemory(k=10, return_messages=True),
        prompt=qa_prompt,
        verbose=True,
        callback_manager=CallbackManager(handlers=[AddressesCallbackManager(addresses),
                                                   StdOutCallbackHandler()])
    )
    return model
