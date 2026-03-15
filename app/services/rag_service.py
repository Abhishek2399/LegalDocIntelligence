"""
Making the file ready to be stored in the vector db by performing below actions
#1 OCR
#2 Chunking
#3 Embedding
"""
import traceback
from app.core.ocr import get_ocr
from app.core.chunker import get_chunks
from app.core.embedder import generate_embeddings


def process_document(file_path:str="")->dict:
    """
    Function that will perform ocr on the file sent to it, split the raw_text from ocr in chunks of overlapping data and then added embeddings to each chunk

    Args:
        file_path (str, optional): Path of the file which needs to be processed. Defaults to "".

    Returns:
        dict: result of the processed document consisting status of each sub-process, final status and the chunks with embeddings
        structure : 
        {
            'embeddings' : <list of chunked data with embeddings>,
            'ocr_status' : <status of ocr>,
            'chunking_status' : <status of chunking>,
            'embedding_status' : <status of embedding>,
            'status' : <final status>,
            'error' : <exception occured if any>
        }
        statuses :
            0 - <Processed but no result>
            -1 - <Error occured>
            1 - <Successful processing>
    """
    result:dict = {
        'embeddings' : [],
        'ocr_status' : 0,
        'chunking_status' : 0,
        'embedding_status' : 0,
        'status' : 0,
        'error' : ''
    }
    raw_text:str = ""
    chunks:list = []
    embedded_chunks:list = []

    # Performing OCR on the file
    try:
        ocr_result = get_ocr(file_path=file_path)
        if ocr_result.get('status') == 1:
            raw_text = ocr_result.get('text')
        result['ocr_status'] = ocr_result.get('status')
    except Exception as e:
        raw_text = ""
        result['error'] = fr"{str(e)}\n{traceback.format_exc()}"
        result['status'] = -1
        result['ocr_status'] = -1
        return result
    
    # Chunking the raw_text with overlaps
    try:
        chunks = get_chunks(raw_text=raw_text)
        if chunks:
            result['chunking_status'] = 1
    except Exception as e:
        result['error'] = fr"{str(e)}\n{traceback.format_exc()}"
        result['status'] = -1
        result['chunking_status'] = -1
        return result


    # Adding embeddings to the chunks
    try:
        embedded_chunks = generate_embeddings(chunks=chunks)
        if embedded_chunks and embedded_chunks[0].get('embedding') :
            result['embedding_status'] = 1
            result['embeddings'] = embedded_chunks
            result['status'] = 1
    except Exception as e:
        result['error'] = fr"{str(e)}\n{traceback.format_exc()}"
        result['status'] = -1
        result['chunking_status'] = -1
        return result
    
    return result
