from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Read API key from environment variable
API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

STOCKS = ["AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA", "NFLX", "NVDA", "ADBE", "INTC"]

@app.route('/')
def home():
    return render_template('index.html', stocks=STOCKS)

@app.route('/price/<symbol>')
def get_stock_price(symbol):
    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    daily = data.get("Time Series (Daily)", {})
    if not daily:
        return jsonify({"error": "Data not found"}), 404
    latest_date = list(daily.keys())[0]
    price = daily[latest_date]["4. close"]
    return jsonify({"symbol": symbol, "price": price})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
