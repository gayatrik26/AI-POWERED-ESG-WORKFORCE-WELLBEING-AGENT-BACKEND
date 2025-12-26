def calculate_burnout(feedback_sentiment, email_sentiment, stress_score, productivity_score):
    """
    Calculate burnout score with stress factor.
    Lower feedback sentiment means higher burnout.
    """
    weights = {
        "feedback_sentiment": 0.2,  
        "email_sentiment": 0.15,
        "stress_score": 0.2,
        "productivity_score": 0.3
    }

    print("burnout-calculator ^^^^^^^^^^^^", 
          "feedback:", feedback_sentiment, 
          "emails:", email_sentiment, 
          "stress:", stress_score,
          "productivity:", productivity_score)

    # Normalize factors
    feedback_factor = 1 - feedback_sentiment  # Lower sentiment means more burnout
    email_factor = 1 - email_sentiment  
    normalized_stress = stress_score / 100  # Convert stress from 0-100 to 0-1

    # Weighted sum burnout calculation
    burnout_score = (
        feedback_factor * weights["feedback_sentiment"] +
        email_factor * weights["email_sentiment"] +
        normalized_stress * weights["stress_score"]  +
        productivity_score * weights["productivity_score"]
    )

    # Ensure burnout score is within 0-1 range
    burnout_score = max(0, min(round(burnout_score, 2), 1)) 

    return burnout_score