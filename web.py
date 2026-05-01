from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET', 'dev-secret')

# Import bot helpers
from bot import place_order, get_client

try:
    from mock_client import MockClient
except Exception:
    MockClient = None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        side = request.form.get('side')
        order_type = request.form.get('type')
        quantity = float(request.form.get('quantity') or 0)
        price_raw = request.form.get('price')
        price = float(price_raw) if price_raw else None
        use_mock = request.form.get('mock') == 'on'

        # Choose client
        if use_mock:
            if MockClient is None:
                return render_template('result.html', error='Mock client not available')
            client = MockClient()
        else:
            client = get_client()

        try:
            order = place_order(client, symbol, side, order_type, quantity, price)
            return render_template('result.html', order=order)
        except Exception as e:
            return render_template('result.html', error=str(e))

    # GET
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
