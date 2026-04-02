import pickle
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "model_transformer.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "encoder.pkl"), "rb") as f:
    encoder = pickle.load(f)

def is_suspicious(text: str) -> bool:
    clean = re.sub(r'[^\w\s]', '', text).strip()
    if not clean:
        return False
    embedding = encoder.encode([text])
    prediction = model.predict(embedding)[0]
    return bool(prediction == 1)

def filter_suspicious(messages: list[dict]) -> list[dict]:
    suspicious = []
    for original_index, msg in enumerate(messages):
        if is_suspicious(msg["text"]):
            msg_with_index = dict(msg)
            msg_with_index["original_index"] = original_index
            suspicious.append(msg_with_index)
    return suspicious