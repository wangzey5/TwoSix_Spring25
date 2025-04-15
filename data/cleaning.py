import pandas as pd
import re
import pickle
import spacy
import gc
import sys
from tqdm import tqdm
from pathlib import Path
from datetime import datetime

# ---------- Text Cleaning ----------
def clean_text(text):
    text = re.sub(r"&#\d+;", " ", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"\\u[0-9A-Fa-f]{4}", "", text)
    text = re.sub(r"[^\w\s.,!?']", "", text)
    text = text.replace('"', '')              
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------- Long Comment Processor ----------
def process_long_comments(comment, threshold=512):
    tokens = comment.split()
    if len(tokens) <= threshold:
        return comment
    split_point = len(tokens) // 4
    return " ".join(tokens[:split_point] + ["..."] + tokens[-split_point:])

# ---------- Filtering ----------
def load_filtered_unique_comments(input_csv, chunksize=10000):
    seen = set()
    filtered_rows = []
    for chunk in pd.read_csv(input_csv, chunksize=chunksize, usecols=[
        'comment', 'agency', 'postedDate', 'docketId', 'commentId', 'documentId'
    ], low_memory=False):
        chunk.dropna(subset=['comment'], inplace=True)
        chunk['comment'] = chunk['comment'].astype(str)
        chunk = chunk[chunk['comment'].str.len() > 10]
        chunk = chunk[~chunk['comment'].str.contains(r"\b(?:attached|attachment)\b", case=False, na=False)]
        chunk['postedDate'] = pd.to_datetime(chunk['postedDate'], errors='coerce')
        chunk = chunk[chunk['postedDate'].dt.year >= 1980]
        chunk = chunk[~chunk['comment'].isin(seen)]
        seen.update(chunk['comment'])
        filtered_rows.append(chunk)
    return pd.concat(filtered_rows).reset_index(drop=True)

# ---------- Chunked Processing ----------
def process_comments_for_sentiment(df, chunk_size=5000, out_dir="processed_chunks", threshold=512):
    Path(out_dir).mkdir(exist_ok=True)
    all_processed = []
    for i in tqdm(range(0, len(df), chunk_size), desc="Chunks", file=sys.stdout):
        chunk = df.iloc[i:i+chunk_size].copy()
        chunk["processed_comment"] = chunk["cleaned_comment"].apply(lambda x: process_long_comments(x, threshold))
        chunk = chunk[["processed_comment", "commentId", "docketId", "documentId", "postedDate", "agency"]]
        all_processed.append(chunk)
    return pd.concat(all_processed).reset_index(drop=True)

# ---------- Main ----------
if __name__ == "__main__":
    input_path = "data/filtered_comments.csv"
    output_path = "data/df_processed.pkl"

    print("📥 Loading and filtering comments...")
    df = load_filtered_unique_comments(input_path)
    df["cleaned_comment"] = df["comment"].apply(clean_text)

    print("✂️ Processing for sentiment...")
    df_processed = process_comments_for_sentiment(df)

    print(f"💾 Saving to {output_path}...")
    df_processed.to_pickle(output_path)
    print("✅ Done! Processed", len(df_processed), "comments.")
