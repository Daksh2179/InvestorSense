from flask import Blueprint

forecast_bp = Blueprint("forecast", __name__)

@forecast_bp.route("/", methods=["GET"])
def test_forecast():
    return {"message": "Forecast route is working (placeholder)"}
