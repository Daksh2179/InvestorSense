from flask import Blueprint, request, jsonify
from database.db import get_connection

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/", methods=["POST"])
def add_portfolio_entry():
    data = request.get_json()
    required_fields = ["ticker", "company_name", "security_type", "buy_price", "quantity", "buy_date", "session_id"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO portfolios (
                ticker, company_name, security_type,
                buy_price, quantity, buy_date, session_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data["ticker"],
            data["company_name"],
            data["security_type"],
            data["buy_price"],
            data["quantity"],
            data["buy_date"],
            data["session_id"]
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Portfolio item saved successfully"}), 201

    except Exception as e:
        print("DB error:", str(e))
        return jsonify({"error": "Database error", "details": str(e)}), 500

@portfolio_bp.route("/", methods=["GET"])
def get_portfolio():
    session_id = request.args.get("session_id")

    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM portfolios WHERE session_id = %s", (session_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        cursor.close()
        conn.close()

        result = [dict(zip(columns, row)) for row in rows]
        return jsonify(result), 200

    except Exception as e:
        print("DB error:", str(e))
        return jsonify({"error": "Database error", "details": str(e)}), 500
