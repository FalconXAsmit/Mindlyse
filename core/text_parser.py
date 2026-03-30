import re

def parse_text_chat(text: str) -> list[dict]:
    messages = []

    pattern = r"\[(\d{1,2}:\d{2}\s?(?:AM|PM))\]\s(\w+):\s(.+)"

    for line in text.strip().splitlines():
        match = re.match(pattern, line)
        if match:
            timestamp, speaker, message = match.groups()
            messages.append({
                "timestamp": timestamp,
                "speaker": speaker,
                "text": message
            })
    
    return messages