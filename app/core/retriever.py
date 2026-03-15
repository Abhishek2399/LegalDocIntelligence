"""
For storing and retrieving the embeddings from the vector DB
"""

import chromadb
import traceback
from app.core.config import VECTOR_STORE_DIR

CLIENT = chromadb.PersistentClient(path=VECTOR_STORE_DIR)
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