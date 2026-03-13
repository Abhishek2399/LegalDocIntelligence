from fastapi import FastAPI
from app.api.routes.documents import router as document_router

app = FastAPI()

# registering the route
app.include_router(document_router, prefix="/document", tags=["Document"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
