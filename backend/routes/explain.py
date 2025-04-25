from flask import Blueprint, request, jsonify
from google_ai import ask_gemini
from forecast_rules import classify_investment
import yfinance as yf

explain_bp = Blueprint("explain", __name__)

@explain_bp.route("/", methods=["GET"])
def explain_investment():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Missing ticker"}), 400

    investment_type = classify_investment(ticker)

    try:
        asset = yf.Ticker(ticker)
        info = asset.info
        name = info.get("shortName", ticker)
        summary = info.get("longBusinessSummary", "")
        sector = info.get("sector", "N/A")

        # For ETFs and funds, fetch top holdings and sectors
        top_holdings_str = ""
        sector_weights_str = ""

        if investment_type in ["etf", "mutual_fund"]:
            holdings = info.get("holdings", [])
            top_holdings = [h.get("holdingName", "") for h in holdings[:5]]
            top_holdings_str = ", ".join(top_holdings) if top_holdings else "Not available"

            sector_weights = info.get("sectorWeightings", [])
            sector_weights_str = ", ".join(
                f"{s['sector']}: {s['weight']*100:.1f}%" for s in sector_weights[:5]
            ) if sector_weights else "Not available"

        prompt = (
            f"Ticker: {ticker.upper()}\n"
            f"Type: {investment_type.replace('_', ' ').title()}\n"
            f"Name: {name}\n"
            f"Summary: {summary}\n"
            f"Sector: {sector}\n"
        )

        if investment_type in ["etf", "mutual_fund"]:
            prompt += (
                f"Top Holdings: {top_holdings_str}\n"
                f"Sector Allocation: {sector_weights_str}\n"
            )

        prompt += (
            "Write a professional, unbiased explanation of this investment's current outlook. "
            "Include comments on diversification, strategy, and investor relevance. Avoid promotional tone."
        )

        response = ask_gemini(prompt)
        return jsonify({
            "ticker": ticker.upper(),
            "type": investment_type,
            "explanation": response.strip()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500