import os
from typing import List, Dict, Union

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


from src.utils import info_str

hf_prefix = "https://huggingface.co/"

def build_cards_retriever(
        cards: Dict[str, str], 
        type: str = 'model',
        vs_type: str = 'chroma',
        emb_type: str = 'openai',
        chunk_size: int = 1000,
        chunk_overlap: int = 0,
        verbose: bool = False,
    ) -> VectorStoreRetriever:
    """Build the vector store retriever for the model cards
    """
    
    # build the docs
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = []
    for k, v in cards.items():
        vs = splitter.split_text(v)
        docs.extend([Document(page_content=x, 
                              metadata={'repo_addr': k, 
                                        'repo_id': k.replace(hf_prefix, ''),
                                        'type': f'{type}_card',
                                        'chunk_size': chunk_size,
                                        'chunk_overlap': chunk_overlap
                                    }) for x in vs])
        
    if verbose: print(info_str(f"Built {len(docs)} documents for {type} cards"))
    
    # build the vectore store db
    if emb_type == 'openai':
        embeddings = OpenAIEmbeddings(
            openai_api_key=os.environ['OPENAI_API_KEY'],
            disallowed_special=()
        )
    else: raise ValueError(f"Invalid embedding type: {emb_type}")
    if vs_type == 'chroma':
        db = Chroma(f'{type}_cards', embeddings)
    else: raise ValueError(f"Invalid vector store type: {vs_type}")
    
    db.add_documents(docs)
    
    # build the retriever
    retriever = db.as_retriever()
    
    if verbose: print(info_str(f"Built the {vs_type} vectore store and the corresponding retriever based on {emb_type} embeddings"))
    
    return retriever


def chat_cards(
        query: str,
        cards: Dict[str, str],
        llm: str = 'gpt-3.5-turbo-1106',
        type: str = 'model',
        mode: str = 'each',
        max_length: int = 10000,
        verbose: bool = False,
    ) -> List[Union[str, Dict[str,str]]]:
    """Chat with the model cards about the query
    """
    prompt_template = PromptTemplate.from_template({
        'each': f"Given the following {type} cards on Hugging Face:\n" + "{card}\n\n" + 
        f"Please answer the question about this certain {type} below:\n" + "{query}\n\nAnswer:",
        'all': "{query}"
    }[mode])
    
    chat_bot = ChatOpenAI(temperature=0.2, model=llm)
    
    responses, failed_cards = [], []
    
    if mode == "each":
        llm_chain = LLMChain(llm=chat_bot, prompt=prompt_template)
        for repo_addr, card in cards.items():
            repo_id = repo_addr.replace(hf_prefix, '')
            if verbose: print(info_str(f"Chatting with the {type} from its card with the repo: {repo_id}"))
            
            try: 
                response = llm_chain.run(query=query, card=card[:max_length])
                responses.append(dict(response=response, repo_addr=repo_addr))
                if verbose: print(response)
            except Exception as e:
                print(info_str(f"Error happened when chatting with {repo_id}", side_str='*'))
                if verbose: print(e)
                failed_cards.append(repo_addr)
            
    elif mode == "all":
        retriever = build_cards_retriever(cards, type=type, verbose=verbose)
        rag_chain = RetrievalQA.from_chain_type(llm=chat_bot, chain_type="stuff", retriever=retriever)
        if verbose: print(info_str(f"Chatting with all the {type}s from their corresponding cards"))
        try: 
            response = rag_chain.run(prompt_template.format(query=query))
            responses.append(response)
            if verbose: print(response)
        except Exception as e:
            print(info_str(f"Error happened when chatting with all the {type}s", side_str='*'))
            if verbose: print(e)
            failed_cards = list(cards.keys())
        
    return responses, failed_cards
            