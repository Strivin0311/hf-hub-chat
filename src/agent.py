import os
from typing import List, Dict



from langchain.vectorstores.base import VectorStoreRetriever
from langchain.agents import tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


from src.utils import info_str
            
            
def build_hf_agent(
        retriever: VectorStoreRetriever,
        llm: str = 'gpt-3.5-turbo-11106',
    ):
    agent_bot = ChatOpenAI(temperature=0.2, model=llm)
    rag_bot = ChatOpenAI(temperature=0.1, model=llm)
    qa_chain = RetrievalQA.from_chain_type(llm=rag_bot, chain_type="stuff", retriever=retriever)
    
    @tool
    def retrieve_answer_for_query(query: str) -> str:
        """retrieve from the documents to get the answer for the user query
        Args:
            query (str): the user query
            
        Returns: 
            answer (str): the answer to the user query based on the retrieved documents
        """
        answer = qa_chain.run(query)
        return answer
        
    hf_agent = initialize_agent(
        tools=[retrieve_answer_for_query], 
        llm=agent_bot, 
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, # the agent just do actions and no more interaction
        handle_parsing_errors=True,
        verbose=True
    )
        
    return hf_agent