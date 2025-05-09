# add_sentiment.py
## This script adds sentiment analysis to the DataFrame using a pre-trained model from Hugging Face.
 
import pandas as pd
import torch
import torch.nn.functional as F
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification

device = "cuda" if torch.cuda.is_available() else "cpu"

def add_sentiment(df, batch_size=256):
    print("💬 Running sentiment analysis (normalized to [-1, 1])")

    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)

    comments = df["processed_comment"].fillna("neutral").tolist()
    sentiment_scores = []
    sentiment_labels = []
    sentiment_texts = []

    label_map_numeric = {0: -1, 1: 0, 2: 1}
    label_map_text = {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}

    for i in tqdm(range(0, len(comments), batch_size), desc="Processing batches"):
        batch = comments[i:i+batch_size]
        try:
            tokens = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512).to("cuda")
            with torch.no_grad():
                outputs = model(**tokens)
                probs = F.softmax(outputs.logits, dim=1)
                scores_batch = (-1 * probs[:, 0] + probs[:, 2]).tolist()
                labels_batch = torch.argmax(probs, dim=1).tolist()

                sentiment_scores.extend(scores_batch)
                sentiment_labels.extend([label_map_numeric[i] for i in labels_batch])
                sentiment_texts.extend([label_map_text[i] for i in labels_batch])
        except Exception as e:
            print(f"⚠️ Batch {i}-{i+batch_size} failed: {e}")
            sentiment_scores.extend([0.0] * len(batch))
            sentiment_labels.extend([0] * len(batch))  # fallback = neutral
            sentiment_texts.extend(["NEUTRAL"] * len(batch))

    df["sentiment_score"] = sentiment_scores
    df["sentiment_label"] = sentiment_labels     # -1 / 0 / 1
    df["sentiment_text"] = sentiment_texts       # NEGATIVE / NEUTRAL / POSITIVE

    print("✅ Sentiment scores added to DataFrame")
    return df