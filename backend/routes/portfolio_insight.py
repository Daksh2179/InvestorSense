from flask import Blueprint, request, jsonify
from google_ai import ask_gemini
from forecast_rules import classify_investment
import yfinance as yf

portfolio_insight_bp = Blueprint("portfolio_insight", __name__)

@portfolio_insight_bp.route("/", methods=["POST"])
def generate_portfolio_insight():
    data = request.get_json()
    tickers = data.get("tickers", [])

    if not tickers or not isinstance(tickers, list):
        return jsonify({"error": "Missing or invalid 'tickers' list"}), 400

    insights = []

    for ticker in tickers:
        asset = yf.Ticker(ticker)
        info = asset.info
        name = info.get("shortName", ticker)
        summary = info.get("longBusinessSummary", "")
        classification = classify_investment(ticker)
        sector = info.get("sector", "N/A")

        insights.append({
            "ticker": ticker.upper(),
            "name": name,
            "type": classification,
            "sector": sector,
            "summary": summary[:500]  # Trim if needed for prompt
        })

    prompt = "The user has the following investments:\n\n"
    for item in insights:
        prompt += (
            f"{item['ticker']} ({item['type']}): {item['name']}\n"
            f"Sector: {item['sector']}\n"
            f"Summary: {item['summary']}\n\n"
        )

    prompt += (
        "Based on this portfolio, provide a calm, two-paragraph financial insight. "
        "Focus on balance, risk exposure, sector diversity, and long-term strength. "
        "Avoid hype. Speak as a financial advisor would to a cautious investor."
    )

    ai_response = ask_gemini(prompt)

    return jsonify({
        "portfolio_analysis": ai_response.strip(),
        "tickers": [t.upper() for t in tickers]
    })
    