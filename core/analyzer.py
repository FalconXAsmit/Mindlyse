from google import genai
from dotenv import load_dotenv
from models.conversation import AnalysisResult
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_conversation(messages: list[dict]) -> AnalysisResult:
    if not messages:
        raise ValueError("No messages to analyze")

    conversation_text = "\n".join(
        [f"{msg['speaker']} [{msg['timestamp']}]: {msg['text']}" for msg in messages]
    )

    prompt = f"""
        You are an expert in psychological manipulation and abusive communication patterns.

        Analyze the following conversation and identify any manipulation tactics present.

        For each message that contains a manipulation tactic, provide:
        - The message index (starting from 0)
        - The speaker
        - The tactic name (e.g. gaslighting, love bombing, DARVO, isolation, intermittent reinforcement, guilt tripping, passive aggression)
        - A brief explanation of why this is a red flag

        Then provide a pattern-level summary of the overall conversation dynamic.

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

        If no manipulation tactics are found, return empty flagged_messages and set severity to "low".

        Conversation:
        {conversation_text}
        """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
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
