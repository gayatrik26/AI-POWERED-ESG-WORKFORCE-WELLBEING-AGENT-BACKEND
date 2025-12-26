from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Mapping RoBERTa LABELs to sentiment categories
LABEL_MAPPING = {
    "LABEL_0": "very_negative",
    "LABEL_1": "neutral",
    "LABEL_2": "very_positive"
}

def analyze_sentiment(text):
    """Analyze sentiment and return {'label': category, 'score': float (-1 to 1)}."""
    
    if not text or not isinstance(text, str):
        return {"label": "neutral", "score": 0.0}  

    result = sentiment_pipeline(text)

    if isinstance(result, list) and len(result) > 0 and "label" in result[0] and "score" in result[0]:
        sentiment_label = result[0]["label"]
        raw_score = result[0]["score"]

        # Convert RoBERTa scores (0 to 1) into range (-1 to 1)
        normalized_score = 2 * raw_score - 1  

        # Assign labels
        if sentiment_label == "LABEL_0":
            label = "very_negative"
        elif sentiment_label == "LABEL_1":
            label = "neutral"
        elif sentiment_label == "LABEL_2":
            label = "very_positive"
        else:
            label = "neutral"
            normalized_score = 0.0  
        
        normalized_score = round(normalized_score, 4)

        return {"label": label, "score": normalized_score}
    
    print(f"ERROR: Unexpected sentiment output: {result}")
    return {"label": "neutral", "score": 0.0}