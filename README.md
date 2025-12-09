# Weixin-Demo-Ecommerce-AI-Agent

## Introduction

A Multilingual E-commerce AI Assistant with Sentiment Analysis, Product Search, Offer Engine & Customer Memory-- This project is a prototype of an AI-powered customer service agent designed for WeChat, Weixin, for e-commerce platforms. It has custom inbuilt tools handles customer reviews, provides personalized offers, fetches product details, and maintains long-term customer interaction history. It is a demo built with LangChain, Ollama, Python, TextBlob, and SQLite, it mimics the behavior of a real customer support representative. UI is created using streamlit for faster inference. At first I used (meta-llama/llama-3.3-70b-instruct:free model) from [Openrouter](https://openrouter.ai/), but later I shifted to Local LLM which are more powerful and faster inference latency from [Ollama](https://ollama.com/). This completely optional.

## Results
<p align="center">
  <img src="https://github.com/Abhigyan9831/Weixin-Demo-Ecommerce-AI-Agent/blob/main/assets/english.png?raw=true" width=50%>
  <img src="https://github.com/Abhigyan9831/Weixin-Demo-Ecommerce-AI-Agent/blob/main/assets/chinese.png?raw=true" width=50%>
</p>

Fig a. Top picture represents the response in Chinese especifically for Chinese/Mandarin speaking people. b. Below picture represents forcing the LLM to respond the response in English.

## Please Note
Due to certain access limitations and API restrictions, I was not able to fully integrate official e-commerce APIs (such as Amazon, Alibaba, AliExpress) or the WeChat/Weixin Customer Service API. These platforms often require special permissions, verified business accounts, paid plans, or region-specific access, which were not available during development. The project remains functional and easy to test, I implemented custom-built tools that simulate the behavior of real APIs in ```tools.py```. These include:
- Custom sentiment analysis tool from customer review.
- Custom offer-generation engine.
- Local database for customer history.
- Local message-processing pipeline (instead of real WeChat API/Weixin API).
This approach allows the system to run fully offline and remain open-source friendly, while still demonstrating, realistic product interactions, personalized offer generation judged by sentiment score, sentiment-based responses, agent memory and workflow automation.
**Future Plans - If API access becomes available in the future, the architecture can be extended easily to connect to real platforms.**






##  The UI 
<p align="center">
  <img src="https://github.com/Abhigyan9831/Weixin-Demo-Ecommerce-AI-Agent/blob/main/assets/main_page.png?raw=true" width=100%>
</p>




