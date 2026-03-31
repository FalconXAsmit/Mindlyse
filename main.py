from fastapi import FastAPI, UploadFile, File, HTTPException
from core.text_parser import parse_text_chat
from core.pdf_parser import parse_pdf_chat
from core.analyzer import analyze_conversation
from models.conversation import Conversation, Message, AnalysisResult

app = FastAPI(
    title="Mindlyse",
    description="AI-powered conversation analysis for detecting psychological manipulation",
    version="0.1.0"
)

SUPPORTED_TYPES = {
    "text/plain": "txt",
    "application/pdf": "pdf"
}

@app.get("/")
def root():
    return {"message": "Mindlyse is alive"}

@app.post("/upload", response_model=Conversation)
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code=400,
            detail= "Unsupported file type. Supported: txt, pdf, png, jpg"
        )

    try:
        contents = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read file")

    file_type = SUPPORTED_TYPES[file.content_type]

    if file_type == "txt":
        text = contents.decode("utf-8")
    elif file_type == "pdf":
        text = parse_pdf_chat(contents)

    raw_messages = parse_text_chat(text)

    if not raw_messages:
        raise HTTPException(status_code=422, detail="No messages found in file")

    messages = [Message(**msg) for msg in raw_messages]
    return Conversation(
        filename=file.filename,
        message_count=len(messages),
        messages=messages
    )

@app.post("/analyze", response_model=AnalysisResult)
async def analyze(file: UploadFile = File(...)):
    if file.content_type not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Supported: txt, pdf, png, jpg"
        )

    try:
        contents = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read file")

    file_type = SUPPORTED_TYPES[file.content_type]

    if file_type == "txt":
        text = contents.decode("utf-8")
    elif file_type == "pdf":
        text = parse_pdf_chat(contents)

    raw_messages = parse_text_chat(text)

    if not raw_messages:
        raise HTTPException(status_code=422, detail="No messages found in file")

    try:
        result = analyze_conversation(raw_messages)
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))