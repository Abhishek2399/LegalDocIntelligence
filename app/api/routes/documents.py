from fastapi import APIRouter, UploadFile, HTTPException, File
from app.core.config import UPLOAD_DIR
from app.core.ocr import get_ocr
import traceback

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    response : dict = {
        'status' : '',
        'filename' : file.filename,
        'raw_text' : '',
        'ocr_status' : '',
        'ocr_method' : '',
        'total_pages' : 0,
        'error' : ''
    }

    # validate it's a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # save file to uploads folder
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:   
        # extracting the raaw_text from the file
        ocr_result = get_ocr(file_path=file_path)
    except Exception as e:
        response['error'] = f"{str(e)}\n{traceback.format_exc()}"
        response['status'] = 'un-successful'
        return response
    

    if ocr_result.get('status', 0) == 1 : 
        response['status'] = 'successful'
        response['raw_text'] = ocr_result.get('text')
        response['ocr_status'] = 1
        response['ocr_method'] = ocr_result.get('method')
        response['total_pages'] = ocr_result.get('page_count')
    elif ocr_result.get('status', 0) == 0 : 
        response['status'] = 'un-successful OCR'
        response['raw_text'] = ocr_result.get('text')
        response['ocr_status'] = 0
        response['ocr_method'] = ocr_result.get('method')
        response['total_pages'] = ocr_result.get('page_count')
    else:
        response['status'] = 'un-successful'
        response['raw_text'] = ''
        response['ocr_status'] = -1
        response['ocr_method'] = ocr_result.get('method')
        response['total_pages'] = ocr_result.get('page_count')
        response['error'] = ocr_result.get('error')

    
    return response
