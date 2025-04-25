import yfinance as yf

# Dynamically classify stock by market cap
def classify_stock(ticker):
    try:
        info = yf.Ticker(ticker).info
        market_cap = info.get("marketCap", 0)

        if market_cap > 200_000_000_000:
            return "blue_chip"
        elif market_cap > 10_000_000_000:
            return "mid_cap"
        else:
            return "small_cap"
    except Exception as e:
        print(f"Error classifying {ticker}: {e}")
        return "unknown"

def classify_investment(ticker):
    ticker = ticker.upper()
    if ticker.endswith("X"):
        return "mutual_fund"
    elif ticker in ["VTI", "VOO", "ARKK", "QQQ"]:  # Expand as needed
        return "etf"
    else:
        return "stock"

# Generate a forecast based on sentiment score + classification
def generate_forecast(ticker, sentiment_score):
    classification = classify_stock(ticker)

    if sentiment_score < -0.6:
        if classification == "blue_chip":
            return {
                "classification": classification,
                "suggestion": "Buy the dip",
                "confidence": "Medium",
                "note": "Long-term stability despite short-term negativity"
            }
        elif classification == "small_cap":
            return {
                "classification": classification,
                "suggestion": "Avoid",
                "confidence": "High",
                "note": "Negative sentiment poses high risk for small caps"
            }
        else:
            return {
                "classification": classification,
                "suggestion": "Hold off",
                "confidence": "Medium",
                "note": "Unclear upside — wait for recovery"
            }
    
    elif sentiment_score > 0.6:
        return {
            "classification": classification,
            "suggestion": "Consider Buying",
            "confidence": "High",
            "note": "Positive market sentiment supports buying"
        }
    
    else:
        return {
            "classification": classification,
            "suggestion": "Hold",
            "confidence": "Neutral",
            "note": "No strong signal to act on"
        }
