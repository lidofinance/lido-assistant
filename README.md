# Lido Assistant

This is a simple tool that can answer the questions about the Lido DAO.
It bases on the https://docs.lido.fi/ content

## How to use

`python main.py console` for the console mode
`python main.py discord` for the discord integration

## TODO

This repo includes two variations of Agent chatbots.

-   src/chat_agent.py: a simple single action thought loop to come up with an answer to questions. It has access to a VectorDB Chain and CoinGecko's public price API. It is limited by only being able to take a single action at a time, increasing the number of LLM calls required for grouped questions.
-   src/agent/multi_action_agent.py: the beginning of a Multi Action Agent which can perform multiple actions at the same time. Includes a custom prompt, custom output parser. It has the benefit of being able to perform multiple operations in a single Thought-Action(s)-Observation loop.

Multi Action Agent currently does not use memory, but it could have it added.
