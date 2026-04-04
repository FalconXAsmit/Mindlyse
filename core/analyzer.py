from google import genai
from models.conversation import AnalysisResult
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ml'))
from ml.classifier import filter_suspicious

def analyze_conversation(messages: list[dict], api_key: str) -> AnalysisResult:
    if not messages:
        raise ValueError("No messages to analyze")

    client = genai.Client(api_key=api_key)

    suspicious_messages = filter_suspicious(messages)

    if not suspicious_messages:
        return AnalysisResult(
            flagged_messages=[],
            pattern_summary="No suspicious messages detected. The conversation appears clean.",
            severity="none",
            dominant_tactic=None
        )

    conversation_text = "\n".join([
        f"[index:{msg['original_index']}] {msg['speaker']} [{msg['timestamp']}]: {msg['text']}"
        for msg in suspicious_messages
    ])

    prompt = f"""
You are an expert in psychological manipulation and abusive communication patterns.

Analyze the following messages which have been pre-screened as potentially manipulative.

For each message that contains a manipulation tactic, provide:
- The message index — use the [index:N] number shown before each message
- The speaker
- The tactic name (e.g. gaslighting, love bombing, DARVO, isolation, intermittent reinforcement, guilt tripping, passive aggression)
- A brief explanation of why this is a red flag

Return your response as valid JSON only, no extra text, in this exact format:
{{
    "flagged_messages": [
        {{
            "message_index": 0,
            "speaker": "name",
            "tactic": "tactic name",
            "explanation": "why this is a red flag"
        }}
    ],
    "pattern_summary": "overall summary of the conversation dynamic",
    "severity": "low | medium | high",
    "dominant_tactic": "the most prominent tactic used"
}}

If no manipulation tactics are found, return:
{{
    "flagged_messages": [],
    "pattern_summary": "No significant manipulation tactics detected.",
    "severity": "none",
    "dominant_tactic": null
}}

Severity guide:
- none: no tactics detected
- low: 1-2 minor instances, could be unintentional
- medium: repeated patterns across multiple messages
- high: systematic, pervasive manipulation throughout

The conversation may be in English, Hindi, Romanised Hindi, or a mix. Analyze accordingly.

Messages to analyze:
{conversation_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        data = json.loads(raw)
        return AnalysisResult(**data)

    except json.JSONDecodeError:
        raise ValueError("Gemini returned invalid JSON, try again")
    except Exception as e:
        raise ValueError(f"Analysis failed: {str(e)}")