from flask import Flask, request, jsonify
from scipy.stats import norm
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows cross-origin requests (from your HTML file)

def bsm_price(option_type, S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type.lower() == 'c':
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type.lower() == 'p':
        price = -S * norm.cdf(-d1) + K * math.exp(-r * T) * norm.cdf(-d2)
    else:
        return None
    return price

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    option_type = data['type']
    S = float(data['spot_price'])
    K = float(data['strike_price'])
    sigma = float(data['volatility'])
    r = float(data['risk_free_rate'])
    T = float(data['time'])

    price = bsm_price(option_type, S, K, T, r, sigma)

    if price is None:
        return jsonify({'error': 'Invalid option type'}), 400

    return jsonify({'price': price})

if __name__ == '__main__':
    app.run(debug=True)