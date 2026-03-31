# Mindlyse

AI - powered conversation analysis for detection of Psychological Manipulation tactics on text.

## What it does
Upload a chat conversation and Mindlyse identifies manipulation tactics like gaslighting, 
love bombing, DARVO, isolation, and intermittent reinforcement — with explanations for 
each flag and a pattern-level summary of the overall dynamic.

## Tech Stack
- Python — everything
- FastAPI — backend
- Google Gemini 2.5 Flash — LLM analysis
- Pydantic — data validation

## Current features
- Text chat file upload and parsing
- Per-message manipulation tactic detection
- Pattern-level conversation summary
- Severity scoring (low, mid, high)
- Dominant tactic identification

## Endpoints
- GET / — health check
- POST /upload — parse a conversation file
- POST /analyze — full manipulation analysis

## Coming soon
- Image support (Maybe)
- Pre-screening ML classifier
- Frontend UI