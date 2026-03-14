"""
Generating embeddings for the chunks
"""
from app.core.config import GEMINI_API_KEY
import google.generativeai as genai
from copy import deepcopy
import traceback


genai.configure(api_key=GEMINI_API_KEY)


def generate_embeddings(chunks:list)->list:
    """
    Function which will generate embeddings for the chunks of documents passed to it

    Args:
        chunks (list): Overlapping Chunks of the document

    Returns:
        list: Updated list of chunks with embeddings in it as a new key 'embedding'
    """
    embeded_chunks = deepcopy(chunks)
    for chunk in embeded_chunks:
        try:
            chunk['embedding'] = genai.embed_content(
                model="models/gemini-embedding-001",
                content=chunk.get("text")
            ).get('embedding', [])
        except Exception as e:
            chunk['embedding'] = []
            chunk['embedding_error'] = f"{str(e)} -> {traceback.format_exc()}"

    return embeded_chunks