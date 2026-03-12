"""
OCR handling using pymupdf and tesseract as fallback
"""

import traceback
from PIL import Image
import pymupdf, pytesseract, io

def get_ocr(file_path:str="")->dict:
    """
    Function which will get the raw text from the document and return a structured response

    Args:
        file_path (str, optional): File path from which we want to extract the raw text. Defaults to "".

    Returns:
        dict: 
        structure : {
        "text": <Extracted text>,
        "method": <Module of extraction>,
        "page_count": <Total pages in the document>,
        "status": < 1 : success, -1 : error in processing , 0 : processed but no extraction>
    }
    """
    text = ""
    result = {
        "text": "",
        "method": "",
        "page_count": 0,
        "status": -1
    }
    if not file_path:
        return {
            "text": "",
            "method": "NA",
            "page_count": 0,
            "status": -1
        }
    try:
        # trying extraction from pymupdf
        doc = pymupdf.open(file_path)
        result['page_count'] = doc.page_count
        for page in doc:
            text += page.get_text()
        
        if text:
            # if text extracted from the pymupdf libarary 
            result['text'] = text
            result['method'] = 'pymupdf'
            result['status'] = 1
        else:
            # trying to extract text from tesseract
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=300)
                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))
                
                # Run Tesseract on the image
                text += f"\n{pytesseract.image_to_string(img)}\n"

            if text:
                result['text'] = text
                result['method'] = 'tesseract'
                result['status'] = 1
            else:
                result['text'] = text
                result['method'] = 'tesseract'
                result['status'] = 0

    except Exception as e:
        result['status'] = -1
        result['error'] = fr"{str(e)}\n{traceback.format_exc()}"
    return result