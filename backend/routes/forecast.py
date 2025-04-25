from flask import Blueprint, request, jsonify
from forecast_rules import generate_forecast
import requests

forecast_bp = Blueprint("forecast", __name__)

@forecast_bp.route("/", methods=["GET"])
def get_forecast():
    ticker = request.args.get("ticker")

    if not ticker:
        return jsonify({"error": "Missing 'ticker' parameter"}), 400

    # Call your internal sentiment API
    try:
        sentiment_response = requests.get(f"http://localhost:5000/api/sentiment/?ticker={ticker}")
        sentiment_data = sentiment_response.json()

        if sentiment_response.status_code != 200 or "articles" not in sentiment_data:
            return jsonify({"error": "Failed to fetch sentiment for ticker"}), 500

        # Compute average sentiment score from articles
        scores = [article["sentiment_score"] for article in sentiment_data["articles"] if "sentiment_score" in article]
        if not scores:
            return jsonify({"error": "No sentiment data found"}), 404

        avg_sentiment = sum(scores) / len(scores)

    except Exception as e:
        return jsonify({"error": f"Sentiment API error: {str(e)}"}), 500

    forecast = generate_forecast(ticker, avg_sentiment)

    return jsonify({
        "ticker": ticker.upper(),
        "sentiment_score": round(avg_sentiment, 4),
        "forecast": forecast
    }), 200
