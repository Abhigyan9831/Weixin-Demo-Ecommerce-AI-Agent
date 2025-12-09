from typing import List, Dict
from textblob import TextBlob
import json
from datetime import datetime
import sqlite3
from langchain_core.tools import tool


@tool
def client_sentiment(review: str) -> str:
    """Analyze the sentiment of a customer review. Returns sentiment classification and scores."""
    analysis = TextBlob(review)
    if analysis.sentiment.polarity > 0.3:
        sentiment = "Positive"
    elif analysis.sentiment.polarity < -0.3:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    result = {
        "sentiment": sentiment,
        "polarity_score": round(analysis.sentiment.polarity, 2),
        "subjectivity_score": round(analysis.sentiment.subjectivity, 2),
        "review": review
    }
    return json.dumps(result)


@tool
def extract_keywords(review: str) -> str:
    """Extract key topics and keywords from a customer review."""
    blob = TextBlob(review.lower())
    product_keywords = ['quality', 'price', 'delivery', 'shipping', 'service', 
                       'customer support', 'product', 'packaging', 'value', 'fast',
                       'slow', 'expensive', 'cheap', 'defective', 'broken', 'excellent']
    
    found_keywords = [word for word in product_keywords if word in review.lower()]
    keywords = found_keywords if found_keywords else ["general feedback"]
    return json.dumps({"keywords": keywords})


@tool
def offer_generate(sentiment_data: str, customer_id: str) -> str:
    """Generate a personalized offer based on customer sentiment and ID."""
    try:
        data = json.loads(sentiment_data)
    except:
        data = {"sentiment": "neutral", "polarity_score": 0}
    
    sentiment = data.get("sentiment", "neutral").lower()
    polarity = data.get("polarity_score", 0)
    
    offers = {
        "negative": {
            "discount": 20,
            "type": "Recovery Discount",
            "message": "We're sorry for your experience! Here's 20% off your next purchase + priority support.",
            "urgency": "24 hours",
            "extras": ["Free shipping", "Priority customer support", "Extended return period"]
        },
        "neutral": {
            "discount": 10,
            "type": "Engagement Offer",
            "message": "Thank you for your feedback! Enjoy 10% off for your next order.",
            "urgency": "7 days",
            "extras": ["Free shipping on orders over $50"]
        },
        "positive": {
            "discount": 5,
            "type": "Loyalty Reward",
            "message": "Thank you for being an amazing customer! Here's 5% off as a token of appreciation.",
            "urgency": "14 days",
            "extras": ["Early access to new products", "VIP customer status"]
        }
    }
    
    offer = offers.get(sentiment, offers["neutral"])
    offer["customer_id"] = customer_id
    offer["generated_at"] = datetime.now().isoformat()
    offer["sentiment_trigger"] = sentiment
    
    return json.dumps(offer)


@tool
def save_interaction(customer_id: str, review: str, sentiment: str, offer: str) -> str:
    """Save customer interaction to database for future reference."""
    conn = sqlite3.connect('wechat_agent_memory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            review_text TEXT,
            sentiment TEXT,
            offer_details TEXT,
            timestamp TEXT
        )
    ''')
    
    cursor.execute('''
        INSERT INTO interactions (customer_id, review_text, sentiment, offer_details, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, review, sentiment, offer, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    return f"Interaction saved successfully for customer {customer_id}"


@tool
def get_customer_history(customer_id: str) -> str:
    """Retrieve past interaction history for a customer."""
    conn = sqlite3.connect('wechat_agent_memory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            review_text TEXT,
            sentiment TEXT,
            offer_details TEXT,
            timestamp TEXT
        )
    ''')
    
    cursor.execute('''
        SELECT review_text, sentiment, offer_details, timestamp 
        FROM interactions 
        WHERE customer_id = ?
        ORDER BY timestamp DESC
        LIMIT 5
    ''', (customer_id,))
    
    history = cursor.fetchall()
    conn.close()
    
    if not history:
        return json.dumps([{"message": "No previous records found"}])
    
    history_list = [
        {
            "review": row[0],
            "sentiment": row[1],
            "offer": row[2],
            "date": row[3]
        }
        for row in history
    ]
    
    return json.dumps(history_list)