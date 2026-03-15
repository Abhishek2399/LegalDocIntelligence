"""
For storing and retrieving the embeddings from the vector DB
"""

import chromadb
import traceback
from app.core.config import VECTOR_STORE_DIR

CLIENT = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
COLLECTION = CLIENT.get_or_create_collection(name="bank_guarantees")


def store_chunk(embedded_chunks:list=None)->dict:
    """
    Function which will store the embeddings in the Vector DB

    Args:
        embedded_chunks (list, optional): List of chunks with their embeddings. Defaults to [].

    Returns:
        dict: Status of the storage 
        structure :
        {
            'status' : <status of the storing process>,
            'error' : <error if any with traceback>
        }
    """
    result = {
        'status' : 0,
        'error' : ''
    }
    if not embedded_chunks:
        result['error'] = f"No data in passed list"
        return result
    
    try:
        COLLECTION.add(
            ids=[f"chunk_{chunk.get('chunk_id')}" for chunk in embedded_chunks],
            embeddings=[chunk.get('embedding') for chunk in embedded_chunks],
            documents=[chunk.get('text') for chunk in embedded_chunks],
        )
        result['status'] = 1
    except Exception as e:
        result['status'] = -1
        result['error'] = fr"{str(e)}\n{traceback.format_exc()}"
        return result
    
    return result


def retrieve(query: str = "", n_results: int = 3) -> dict:
    """
    Function which will restrieve chunks on the basis of the query passed to it

    Args:
        query (str, optional): Query passed for the document. Defaults to "".
        n_results (int, optional): Top n results. Defaults to 3.

    Returns:
        dict: Status of the processing along with chunks and distances for the top n_results
        structure : 
        {
            'chunks' : <chunks relevant to the query>,
            'distances' : <distances of the relevant chunks>,
            'embedding_status' : <status for query embedding>,
            'query_status' : <status for data retrieval>,
            'status' : <overall status>,
            'error' : <error if any>  
        }
    """
    result = {
        'chunks' : [],
        'distances' : [],
        'embedding_status' : 0,
        'query_status' : 0,
        'status' : 0,
        'error' : ''   
    }
    if not query:
        result['error'] = 'No query passed'
        return result
    
    # embedding the passed query
    try:
        embedded_query = genai.embed_content(
            model="models/gemini-embedding-001",
            content=query
        ).get('embedding', [])
        if embedded_query : 
            result['embedding_status'] = 1
    except Exception as e:
        result['status'] = -1
        result['embedding_status'] = -1
        result['error'] = fr"{str(e)}-{traceback.format_exc()}"
        return result

    # retrieving the chunks relevant to the query
    try:
        probable_chunks = collection.query(
            query_embeddings=[embedded_query],
            n_results=n_results
        )
        result['query_status'] = 1
    except Exception as e:
        result['status'] = -1
        result['query_status'] = -1
        result['error'] = fr"{str(e)}-{traceback.format_exc()}"
        return result

    result['chunks'] = probable_chunks.get('documents')
    result['distances'] = probable_chunks.get('distances')
    result['status'] = 1

    return result
