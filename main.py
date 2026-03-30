from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Mindlyse is alive"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return{
        "filename": file.filename,
        "size_bytes": len(contents),
        "content_type": file.content_type
    }