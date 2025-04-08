import re
import pandas as pd
import nltk
import spacy

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

# Download once if needed
nltk.download('punkt')
nltk.download('stopwords')

# Load once
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

def load_filtered_unique_comments(input_csv, chunksize=10000):
    seen = set()
    filtered_comments = []

    for chunk in pd.read_csv(input_csv, chunksize=chunksize, usecols=['comment'], low_memory=False):
        chunk.dropna(subset=['comment'], inplace=True)
        chunk['comment'] = chunk['comment'].astype(str)
        chunk.drop_duplicates(subset=['comment'], inplace=True)

        # Filter out short comments
        chunk = chunk[chunk['comment'].str.len() > 10]
        
        # Remove comments that contain "attached"/"attachment"
        pattern = r'\b(?:attached|attachment)\b'
        chunk = chunk[~chunk['comment'].str.contains(pattern, case=False, na=False)]

        # Remove already seen
        chunk = chunk[~chunk['comment'].isin(seen)]

        seen.update(chunk['comment'])
        filtered_comments.extend(chunk['comment'].tolist())

    return pd.DataFrame(filtered_comments, columns=['comment'])

def clean_text(text):
    """Clean text by removing HTML, unicode, special chars, etc."""
    text = re.sub(r"&#\d+;", " ", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"\\u[0-9A-Fa-f]{4}", "", text)
    text = re.sub(r"[^\w\s.,!?']", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def sentencize_and_filter(comment):
    """Split comment into cleaned, stopword-filtered sentences."""
    sentences = sent_tokenize(comment)
    filtered_sentences = []

    for sent in sentences:
        doc = nlp(sent)
        filtered = " ".join([token.text for token in doc if token.text.lower() not in stop_words])
        if len(filtered.split()) > 3:
            filtered_sentences.append(filtered)

    return filtered_sentences

def generate_clean_sentence_df(input_csv):
    """Full pipeline from raw comments CSV → flat sentence DataFrame"""
    df = load_filtered_unique_comments(input_csv)
    df["cleaned_comment"] = df["comment"].apply(clean_text)
    df["sentences"] = df["cleaned_comment"].apply(sentencize_and_filter)
    flattened_sentences = [sentence for sublist in df["sentences"] for sentence in sublist]
    df_sentences = pd.DataFrame(flattened_sentences, columns=["sentence"])
    return df_sentences

if __name__ == "__main__":
    input_path = "../data/filtered_comments.csv"
    df_sentences = generate_clean_sentence_df(input_path)
    print("✅ Final sentence dataframe shape:", df_sentences.shape)
