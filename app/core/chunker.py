from typing import List

def get_chunks(raw_text:str="") -> List:
    """
    Function to convert raw text into overlapping chunks

    Args:
        raw_txt (str, optional): Extracted OCR raw text. Defaults to "".

    Returns:
        List: list of dictionary with chunks in it
        Structure -> [
            {
                "chunk_id": <chunk_idx>, "text": <chunked_text>, "char_start": <chunk_start_idx>,
            }
        ]
    """
    char_start = 0
    chunk_size = 500
    chunk_overlap = 50
    char_end = char_start + chunk_size
    chunks:list = []
    chunk_idx = 0
    while not (char_start > len(raw_text)):
        chunks.append(
            {
                "chunk_id" : chunk_idx,
                "text" : raw_text[char_start : char_end],
                "char_start" : char_start
            }
        )
        char_start = char_end - 50
        char_end = min(char_start + chunk_size, len(raw_text))
        chunk_idx += 1
    return chunks