import numpy as np
import yfinance as yf
import datetime as dt
import pickle
from flask import Flask, jsonify
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  
crypto_currency = 'BTC'
against_currency = 'USD'

PREDICTION_DAYS = 60
TICKER = f"{crypto_currency}-{against_currency}"  

print("=> Carregando modelo Keras 'bitcoin_lstm_model'...")
try:
    model = load_model("bitcoin_lstm_model")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print("Certifique-se de executar 'requirements.txt' primeiro.")
    exit()

print("=> Carregando scaler 'scaler.pkl'...")
try:
    with open("scaler.pkl", "rb") as f:
        scaler: MinMaxScaler = pickle.load(f)
except Exception as e:
    print(f"Erro ao carregar o scaler: {e}")
    print("Certifique-se de executar 'train.py' primeiro.")
    exit()


@app.get("/api/predict")  
def predict():
    try:
        end_date = dt.datetime.now()
        start_date = end_date - dt.timedelta(days=PREDICTION_DAYS + 30)

        data = yf.download(TICKER, start_date, end_date, progress=False)
        if data.empty:
            return jsonify({"error": "Não foi possível buscar dados do yfinance."}), 500

        actual_value = float(data['Close'].iloc[-1])

        real_data = data['Close'].values[-PREDICTION_DAYS:]
        if len(real_data) < PREDICTION_DAYS:
            return jsonify({
                "error": f"Dados insuficientes para predição. Necessário: {PREDICTION_DAYS}, Obtido: {len(real_data)}"
            }), 400

        scaled_input = scaler.transform(real_data.reshape(-1, 1))
        x_input = scaled_input.reshape(1, PREDICTION_DAYS, 1)

        predicted_price_scaled = model.predict(x_input, verbose=0)
        prediction_value = float(scaler.inverse_transform(predicted_price_scaled)[0][0])

        delta = prediction_value - actual_value
        flutation = "Alta" if delta > 0 else ("Queda" if delta < 0 else "Manteve")

        return jsonify({
            "ticker": TICKER,
            "actual_value": actual_value,
            "prediction_value": prediction_value,
            "flutation": flutation
        })
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
