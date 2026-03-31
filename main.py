from fastapi import FastAPI, UploadFile, File
from core.text_parser import parse_text_chat
from models.conversation import Conversation, Message

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Mindlyse is alive"}

@app.post("/upload", response_model=Conversation)
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    text = contents.decode("utf-8")
    raw_messages = parse_text_chat(text)

    messages = [Message(**msg) for msg in raw_messages]

    return Conversation(
        filename = file.filename,
        message_count = len(messages),
        messages = messages
    )