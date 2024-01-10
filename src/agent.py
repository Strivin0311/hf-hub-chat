from langchain.agents import tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI


def get_hf_agent(
        llm: str = 'gpt-3.5-turbo-11106',
    ):
    agent_bot = ChatOpenAI(temperature=0.0, model=llm)

    hf_agent = initialize_agent(
        tools=[], 
        llm=agent_bot, 
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, # the agent just do actions and no more interaction
        handle_parsing_errors=True,
        verbose=True
    )
        
    return hf_agent