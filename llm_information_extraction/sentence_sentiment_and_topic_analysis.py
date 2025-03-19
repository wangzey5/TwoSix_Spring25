import json
from typing import List, Literal
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


LM_STUDIO_API_BASE = os.getenv("LM_STUDIO_API_BASE")
MODEL_NAME = "meta-llama-3.1-8b-instruct"  # Change to your loaded model


class SentimentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(
        description="Confidence Score between 0 and 1",
        ge=0, le=1
    )


class TopicAnalysis(BaseModel):
    """Classification of the main topic in a sentence."""
    topics: List[str] = Field(
        description="List of topics found in the sentence")
    primary_topic: str = Field(description="The main topic of the sentence")


class SentenceAnalysis(BaseModel):
    sentiment: SentimentAnalysis
    topics: TopicAnalysis


ResponseSchema = response_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "sentence_analysis",
        "schema": {
            "type": "object",
            "properties": {
                "sentiment": {
                    "type": "object",
                    "properties": {
                        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                    },
                    "required": ["sentiment", "confidence"]
                },
                "topics": {
                    "type": "object",
                    "properties": {
                        "topics": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "primary_topic": {"type": "string"}
                    },
                    "required": ["topics", "primary_topic"]
                }
            },
            "required": ["sentiment", "topics"]
        }
    }
}


def analyze_sentence(sentence, llm):
    prompt = f"""
    You are a sentence Analyzer system. Do not use any code. Just directly five the output in json. Analyze the following sentence and return the result in this JSON structure:
    {{
        "sentiment": {{
            "sentiment": "positive" | "negative" | "neutral",
            "confidence": float (0-1)
        }},
        "topics": {{
            "topics": ["topic1", "topic2"],
            "primary_topic": "main topic"
        }}
    }}
    """

    # Send the prompt to the model
    response = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=f"Sentence: {sentence}")
    ])
    # Try parsing the response into the SentenceAnalysis schema
    try:
        parsed_response = json.loads(response.content)
        # Use Pydantic model to validate the structure
        return SentenceAnalysis(**parsed_response)
    except Exception as e:
        print(f"Error parsing response: {e}")
        return response.content


if __name__ == "__main__":
    print(SentenceAnalysis.model_json_schema())
    llm = ChatOpenAI(
        base_url=LM_STUDIO_API_BASE,
        api_key="lm-studio",
        model=MODEL_NAME,  # This is a placeholder name for LM Studio
        temperature=0,
        max_retries=3,
        response_format=ResponseSchema
    )

    # llm_sentence_analyser = llm.with_structured_output(SentenceAnalysis)
    sentences = [
        "I love this product!",
        "This is the worst experience I've ever had.",
        "It's okay, not great but not bad either."
    ]
    for sentence in sentences:
        output = analyze_sentence(sentence, llm)
        print(output)
        print("\n\n\n")
