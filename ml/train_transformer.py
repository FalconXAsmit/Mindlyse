# ml/train_transformer.py
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import sys
import os
sys.path.append(os.path.dirname(__file__))
from data import messages

texts = [m[0] for m in messages]
labels = [m[1] for m in messages]

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

print("loading multilingual model...")
encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

print("encoding training data...")
X_train_enc = encoder.encode(X_train)
X_test_enc = encoder.encode(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_enc, y_train)

predictions = model.predict(X_test_enc)
print(classification_report(y_test, predictions, target_names=["normal", "manipulative"]))

with open("model_transformer.pkl", "wb") as f:
    pickle.dump(model, f)

with open("encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("transformer model and encoder saved")