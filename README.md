# 🧠 Mindlyse
 
AI-powered conversation analysis for detecting psychological manipulation tactics.
 
Mindlyse analyzes uploaded conversations and identifies manipulation tactics like gaslighting, love bombing, DARVO, isolation, and intermittent reinforcement — with per-message explanations and a pattern-level summary of the overall dynamic.

---
 
## What it does
 
Upload a chat conversation (WhatsApp export or plain text) and Mindlyse:
 
- Pre-screens every message using a locally trained multilingual classifier
- Sends only suspicious messages to Gemini for deep psychological analysis
- Returns per-message tactic identification with explanations
- Generates a pattern-level summary of the overall conversation dynamic
- Assigns a severity rating: `none`, `low`, `medium`, or `high`
- Handles English, Hindi, and Romanised Hindi (Hinglish)
 
---
 
## Architecture
 
```
Uploaded file
     │
     ▼
File Parser (txt / WhatsApp export / PDF)
     │
     ▼
Multilingual Pre-screening Classifier
(paraphrase-multilingual-MiniLM-L12-v2 + Logistic Regression)
     │
     ├── Clean messages → skipped (no API call)
     │
     └── Suspicious messages → Gemini 2.5 Flash
                                      │
                                      ▼
                              Structured JSON Analysis
                              (tactics, explanations, summary, severity)
```
 
The two-stage pipeline means only suspicious messages hit the LLM — reducing latency, API costs, and unnecessary calls on clean conversations.
 
---
 
## Tech stack
 
| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| Pre-screening | Sentence Transformers + Scikit-learn |
| Embeddings | `paraphrase-multilingual-MiniLM-L12-v2` |
| Data validation | Pydantic |
| File parsing | pdfplumber, regex |
| Language | Python 3.11+ |
 
---
 
## ML classifier
 
The pre-screening classifier is trained on 773 labeled examples of manipulative and normal messages — including English and Hinglish examples. It uses a multilingual sentence transformer to generate embeddings, fed into a Logistic Regression classifier.
 
**Current metrics:**
- Accuracy: 84%
- Manipulative recall: 88% (catches 88% of actual manipulation)
- Normal precision: 87%
 
The classifier handles:
- English manipulation patterns (gaslighting, DARVO, love bombing, isolation, guilt tripping)
- Hinglish manipulation patterns (Romanised Hindi)

---
 
## Supported file formats

- WhatsApp `.txt` exports (with mention tags, media omitted lines, system messages automatically handled)
- `.pdf` — PDF chat exports

---
 
## Detected tactics
 
- Gaslighting
- Love bombing
- DARVO (Deny, Attack, Reverse Victim and Offender)
- Isolation
- Intermittent reinforcement
- Guilt tripping
- Passive aggression
- Threat of abandonment
- Victim playing
- Blame shifting
- Conditional affection
- And more — Gemini identifies tactics based on context, not a fixed list

---
 
## Project structure
 
```
mindlyse/
├── core/
│   ├── text_parser.py       # WhatsApp + custom format parser
│   ├── pdf_parser.py        # PDF text extraction
│   ├── image_parser.py      # OCR for screenshots
│   └── analyzer.py          # Gemini analysis pipeline
├── ml/
│   ├── __init__.py
│   ├── data.py              # 773 labeled training examples
│   ├── train.py             # TF-IDF baseline trainer
│   ├── train_transformer.py # Multilingual transformer trainer
│   ├── classifier.py        # Inference interface
│   ├── model_transformer.pkl
│   └── encoder.pkl
├── models/
│   └── conversation.py      # Pydantic schemas
├── main.py                  # FastAPI app
├── app.py                   # Streamlit frontend
├── run.py                   # Run both servers together
└── .env                     # API keys (not committed)
```
 
---
 
 ### Installation
 
```bash
# clone the repo
git clone https://github.com/FalconXAsmit/Mindlyse.git
cd Mindlyse
 
# create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
 
# install dependencies
pip install fastapi uvicorn python-multipart pydantic
pip install google-genai python-dotenv
pip install scikit-learn sentence-transformers
pip install pdfplumber pytesseract Pillow
pip install streamlit requests praw
```
 
### Train the classifier
 
```bash
cd ml
python train_transformer.py
cd ..
```
 
This generates `model_transformer.pkl` and `encoder.pkl`.
 
### Run
 
```bash
python run.py
```

## Usage
 
1. Open `http://localhost:8501`
2. Paste your Gemini API key in the sidebar (get one free at [aistudio.google.com](https://aistudio.google.com))
3. Upload a conversation file
4. Click Analyze
 
Your conversation is never stored. Analysis is ephemeral — processed in memory and discarded immediately.
 
---
 
## Privacy
 
- No conversation data is stored anywhere
- API keys are passed per-request and never persisted
- All processing is ephemeral — data exists only in memory during analysis
- BYOK (Bring Your Own Key) — users supply their own Gemini API key
 
---

## Author
 
Built by [FalconXAsmit](https://github.com/FalconXAsmit)