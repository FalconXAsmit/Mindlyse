import re

SKIP_PATTERNS = [
    r"end-to-end encrypted",
    r"<Media omitted>",
    r"Messages and calls",
    r"missed voice call",
    r"missed video call",
    r"This message was deleted",
    r"You deleted this message",
    r"You created this group",
    r"added you",
    r"changed the subject",
    r"changed this group",
    r"left$",
    r"joined using this group",
]

def clean_message(text: str) -> str:
    text = re.sub(u"@\u2068[^\u2069]*\u2069", "", text)
    text = re.sub(r"@\w+", "", text)
    return text.strip()

def parse_text_chat(text: str) -> list[dict]:
    messages = []

    pattern_custom = r"\[(\d{1,2}:\d{2}\s?(?:AM|PM))\]\s(\w+):\s(.+)"

    pattern_whatsapp = r"\d{1,2}/\d{1,2}/\d{2,4},\s(\d{1,2}:\d{2}\s?(?:AM|PM|am|pm))\s-\s([^:]+):\s(.+)"

    for line in text.strip().splitlines():
        if any(re.search(p, line, re.IGNORECASE) for p in SKIP_PATTERNS):
            continue

        match = re.match(pattern_custom, line)
        if not match:
            match = re.match(pattern_whatsapp, line)

        if match:
            timestamp, speaker, message = match.groups()
            cleaned = clean_message(message)

            # skip if message is empty after cleaning
            if not cleaned:
                continue

            messages.append({
                "timestamp": timestamp.strip(),
                "speaker": speaker.strip(),
                "text": cleaned
            })

    return messages