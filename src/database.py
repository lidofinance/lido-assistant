import json
import os

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import Chroma

from src.loaders import DocsLoader, get_addresses_from_docs, replace_addresses_with_aliases_in_docs


def get_database():
    embeddings = OpenAIEmbeddings()
    if os.path.exists(".store"):
        db = Chroma(persist_directory=".store", embedding_function=embeddings)
        addresses = json.load(open(".store/addresses.json"))
        return db, addresses

    loaders = [DocsLoader(["https://docs.lido.fi",
                           "https://docs.lido.fi/deployed-contracts/goerli/"])]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    addresses = get_addresses_from_docs(docs)
    os.mkdir(".store")
    with open(".store/addresses.json", "w") as f:
        json.dump(addresses, f)
    docs = replace_addresses_with_aliases_in_docs(docs, addresses)
    [doc.metadata.pop("html") for doc in docs]

    texts = TokenTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(docs)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embedding=embeddings, persist_directory=".store")
    db.persist()
    return db, addresses
