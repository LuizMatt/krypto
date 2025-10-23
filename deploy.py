import numpy as np
import yfinance as yf
import datetime as dt
import pickle
from flask import Flask, jsonify
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

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
        scaler = pickle.load(f)
except Exception as e:
    print(f"Erro ao carregar o scaler: {e}")
    print("Certifique-se de executar 'train.py' primeiro.")
    exit()



@app.route("/predict", methods=["GET"])
def predict():
    """
    Endpoint para prever o preço do Bitcoin no próximo dia.
    Ele busca os dados mais recentes, processa e retorna a previsão.
    """
    try:
        end_date = dt.datetime.now()
        start_date = end_date - dt.timedelta(days=PREDICTION_DAYS + 30)
        
        data = yf.download(TICKER, start_date, end_date)

        actual_value = float(data['Close'].iloc[-1])
        
        if data.empty:
            return jsonify({"error": "Não foi possível buscar dados do yfinance."}), 500

        real_data = data['Close'].values[-PREDICTION_DAYS:]
        
        if len(real_data) < PREDICTION_DAYS:
            return jsonify({
                "error": f"Dados insuficientes para predição. Necessário: {PREDICTION_DAYS}, Obtido: {len(real_data)}"
            }), 400

        scaled_input = scaler.transform(real_data.reshape(-1, 1))

        x_input = scaled_input.reshape(1, PREDICTION_DAYS, 1)

        predicted_price_scaled = model.predict(x_input)

        predicted_price = scaler.inverse_transform(predicted_price_scaled)

        prediction_value = float(predicted_price[0][0])

        flutation = ''

        if(prediction_value-actual_value > 0 ):
            flutation = "Alta"
        elif (prediction_value-actual_value < 0):
            flutation = "Queda"
        else :
            flutation = "Manteve"

        return jsonify({
            "ticker": TICKER,
            "actual_value": actual_value,
            "prediction_value": prediction_value,
            "flutation": flutation
        })

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
