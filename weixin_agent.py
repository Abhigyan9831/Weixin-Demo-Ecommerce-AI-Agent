from langchain_ollama import ChatOllama 
from langchain.agents import create_agent
from langchain_core.tools import tool
from textblob import TextBlob
from tools import client_sentiment, extract_keywords, offer_generate, save_interaction, get_customer_history
import sqlite3
from datetime import datetime
from typing import Dict, List
import json
import os

class weixinAgent:
    def __init__(self, api_key: str = None):
        
        self.llm = ChatOllama(
            model="qwen3:1.7B", 
            temperature=0.7,
            num_predict=500,
             

   )
        
        self.tools = [
            client_sentiment,
            extract_keywords,
            offer_generate,
            save_interaction,
            get_customer_history
        ]
        
        
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt="""You are a weixin customer service AI agent for an e-commerce company.

Your job:
1. Analyze customer reviews for sentiment
2. Extract key issues or praise points
3. Generate personalized offers to retain/reward customers
4. Save all interactions for future reference

Rules:
- ALWAYS check customer history first to personalize response
- For NEGATIVE sentiment: offer bigger discounts (20-25%) + extras
- For NEUTRAL sentiment: offer moderate incentives (15%)
- For POSITIVE sentiment: reward loyalty (10%) + VIP perks
- Be empathetic and professional
- Use tools in logical order: history → sentiment → keywords → offer → save

Respond in a friendly, conversational WeChat/Weixin style. You should also ask clarifying questions if needed.""",
        )
    
    def process_review(self, customer_id: str, review_text: str) -> str:
        
        input_text = f"""
Customer ID: {customer_id}
Review: "{review_text}"

Please:
1. Check if this customer has history with us
2. Analyze the sentiment of their review
3. Extract key topics they mentioned
4. Generate an appropriate personalized offer
5. Save this interaction
6. Respond to the customer in a warm, professional way with the offer details 
"""
        
        response = self.agent.invoke({
            "messages": [{"role": "user", "content": input_text}]
        })
        
        
        final_message = response["messages"][-1]
        return final_message.content
    
'''if __name__ == "__main__":
    
    agent = weixinAgent()
    
    test_reviews = [
        {
            "customer_id": "WX_12345",
            "review": "The product quality is terrible! It broke after 2 days. Very disappointed with the delivery time too."
        },
        {
            "customer_id": "WX_67890",
            "review": "Pretty average. The product works but nothing special. Expected more for the price."
        },
        {
            "customer_id": "WX_12345",  
            "review": "Thank you for the discount! This time the product is much better. Great customer service!"
        }
    ]
    
    for i, test in enumerate(test_reviews, 1):
        
        print(f"REVIEW #{i}")
        print(f"Customer: {test['customer_id']}")
        print(f"Review: {test['review']}")

        print("AGENT RESPONSE:")
        print(f"{'─'*80}\n")
            
        response = agent.process_review(
            customer_id=test['customer_id'],
            review_text=test['review']
        )
            
        print(response)
        print(f"\n{'='*80}\n")'''