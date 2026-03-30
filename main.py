from fastapi import FastAPI, UploadFile, File
from core.text_parser import parse_text_chat

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Mindlyse is alive"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode("utf-8")
    messages = parse_text_chat(text)
    return {
        "filename": file.filename,
        "message_count": len(messages),
        "messages": messages
    }