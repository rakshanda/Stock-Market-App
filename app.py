from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = "KNV8I6IPKC1LQ6YO"
BASE_URL = "https://www.alphavantage.co/query"

# List of 10 stock symbols
STOCKS = ["AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA", "NFLX", "NVDA", "ADBE", "INTC"]

@app.route('/')
def home():
    return render_template('index.html', stocks=STOCKS)

@app.route('/price/<symbol>')
def get_stock_price(symbol):
    params = {"function": "TIME_SERIES_DAILY", "symbol": symbol, "apikey": API_KEY}
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
