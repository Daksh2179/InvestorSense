from flask import Flask
from flask_cors import CORS

# Import route blueprints
from routes.portfolio import portfolio_bp
from routes.sentiment import sentiment_bp
from routes.forecast import forecast_bp
from routes.sentiment import sentiment_bp
from routes.explain import explain_bp
from routes.portfolio_insight import portfolio_insight_bp
from routes.holdings import holdings_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(portfolio_bp, url_prefix="/api/portfolio")
app.register_blueprint(sentiment_bp, url_prefix="/api/sentiment")
app.register_blueprint(forecast_bp, url_prefix="/api/forecast")
app.register_blueprint(explain_bp, url_prefix="/api/explain")
app.register_blueprint(portfolio_insight_bp, url_prefix="/api/portfolio/insight")
app.register_blueprint(holdings_bp, url_prefix="/api/holdings")

@app.route("/")
def home():
    return "InvestorSense Backend is running!"

if __name__ == "__main__":
    app.run(debug=True)
