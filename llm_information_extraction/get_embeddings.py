import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

LM_STUDIO_API_BASE = os.getenv("LM_STUDIO_API_BASE")
# use only models that support embedding
MODEL_NAME = "text-embedding-nomic-embed-text-v1.5"


if __name__ == "__main__":

    url = os.path.join(LM_STUDIO_API_BASE, "embeddings")
    text = "This is a sample text to get embeddings."

    payload = {
        "input": text,
        "model": MODEL_NAME
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        embeddings = response.json().get("data", [])
        print("Embeddings:", embeddings)
    else:
        print(f"Error: {response.status_code}, {response.text}")
