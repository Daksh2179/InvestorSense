from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

sentiment_bp = Blueprint("sentiment", __name__)
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# Load the HuggingFace sentiment model
sentiment_pipeline = pipeline("sentiment-analysis")

# Fetch news and score sentiment for each headline
def fetch_news_with_sentiment(ticker):
    url = f"https://gnews.io/api/v4/search?q={ticker}+stock&lang=en&token={GNEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    articles = data.get("articles", [])
    results = []

    for article in articles:
        title = article["title"]
        sentiment = sentiment_pipeline(title)[0]  # Run NLP model
        results.append({
            "title": title,
            "url": article["url"],
            "source": article["source"]["name"],
            "published_at": article["publishedAt"],
            "sentiment_label": sentiment["label"],
            "sentiment_score": sentiment["score"]
        })

    return results

# Route: /api/sentiment?ticker=TSLA
@sentiment_bp.route("/", methods=["GET"])
def get_sentiment():
    ticker = request.args.get("ticker")

    if not ticker:
        return jsonify({"error": "Missing 'ticker' parameter"}), 400

    articles = fetch_news_with_sentiment(ticker)

    if not articles:
        return jsonify({"message": "No recent news found for this ticker."}), 200

    return jsonify({
        "ticker": ticker.upper(),
        "article_count": len(articles),
        "articles": articles
    }), 200
