from flask import Blueprint, request, jsonify
import yfinance as yf

holdings_bp = Blueprint("holdings", __name__)

@holdings_bp.route("/", methods=["GET"])
def get_holdings():
    ticker = request.args.get("ticker", "").upper()
    if not ticker:
        return jsonify({"error": "Missing ticker parameter"}), 400

    try:
        fund = yf.Ticker(ticker)
        fund_info = fund.info
        top_holdings = fund_info.get("holdings", [])  # works for some ETFs

        # If this fails, try .info["topHoldings"] which contains symbol/weight
        if not top_holdings:
            top_holdings = fund_info.get("topHoldings", [])

        if not top_holdings:
            return jsonify({"error": f"No holdings data found for {ticker}"}), 404

        return jsonify({
            "ticker": ticker,
            "name": fund_info.get("shortName", ticker),
            "top_holdings": top_holdings
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
