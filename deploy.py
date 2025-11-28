import numpy as np
import yfinance as yf
import datetime as dt
import pickle
import os
from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

app = Flask(__name__)

PREDICTION_DAYS = 60

ASSETS_CONFIG = {
    'BTC-USD': {
        'model_path': 'BTC_model',
        'scaler_features_path': 'scaler_btc_features.pkl', 
        'scaler_target_path': 'scaler_btc_target.pkl'      
    },
    'ETH-USD': {
        'model_path': 'ETH_model',
        'scaler_features_path': 'scaler_eth_features.pkl',
        'scaler_target_path': 'scaler_eth_target.pkl'
    },
    'DOGE-USD': {
        'model_path': 'DOGE_model',
        'scaler_features_path': 'scaler_doge_features.pkl',
        'scaler_target_path': 'scaler_doge_target.pkl'
    }
}

loaded_assets = {}

def load_assets():
    for ticker, paths in ASSETS_CONFIG.items():
        try:
            if not os.path.exists(paths['model_path']):
                continue
            model = load_model(paths['model_path'])
            
            if not os.path.exists(paths['scaler_features_path']):
                continue
            with open(paths['scaler_features_path'], "rb") as f:
                scaler_features = pickle.load(f)

            if not os.path.exists(paths['scaler_target_path']):
                continue
            with open(paths['scaler_target_path'], "rb") as f:
                scaler_target = pickle.load(f)

            loaded_assets[ticker] = {
                "model": model,
                "scaler_features": scaler_features,
                "scaler_target": scaler_target
            }
            
        except Exception as e:
            print(f"Error loading {ticker}: {e}")

load_assets()

@app.route("/predict", methods=["GET"])
def predict():
    try:
        ticker = request.args.get('symbol', 'BTC-USD').upper()

        if ticker not in loaded_assets:
            return jsonify({
                "error": f"Modelo para '{ticker}' não está disponível.",
                "available_tickers": list(loaded_assets.keys())
            }), 404

        model = loaded_assets[ticker]['model']
        scaler_feat = loaded_assets[ticker]['scaler_features']
        scaler_targ = loaded_assets[ticker]['scaler_target']

        end_date = dt.datetime.now()
        start_date = end_date - dt.timedelta(days=PREDICTION_DAYS + 30)
        
        data = yf.download(ticker, start_date, end_date, progress=False)

        if data.empty:
            return jsonify({"error": "Falha ao buscar dados no Yahoo Finance."}), 500

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        recent_data = data[['Close', 'Volume']].tail(PREDICTION_DAYS)
        
        if len(recent_data) < PREDICTION_DAYS:
            return jsonify({"error": f"Dados insuficientes. Necessário {PREDICTION_DAYS} dias."}), 400

        last_close = recent_data['Close'].iloc[-1]
        actual_value = float(last_close.item()) if hasattr(last_close, 'item') else float(last_close)

        input_df = pd.DataFrame(index=recent_data.index)
        input_df['close'] = recent_data['Close']
        input_df['volume'] = recent_data['Volume']
        
        input_df['edit_count'] = 0.5
        input_df['sentiment_mean'] = 0.0
        input_df['neg_sentiment_ratio'] = 0.0

        input_values = input_df[['close', 'volume', 'edit_count', 'sentiment_mean', 'neg_sentiment_ratio']].values
        
        scaled_input = scaler_feat.transform(input_values)
        
        x_input = scaled_input.reshape(1, PREDICTION_DAYS, 5)
        
        predicted_price_scaled = model.predict(x_input, verbose=0)
        
        predicted_price = scaler_targ.inverse_transform(predicted_price_scaled)
        prediction_value = float(predicted_price[0][0])

        diff = prediction_value - actual_value
        threshold = actual_value * 0.0005

        if diff > threshold:
            flutation = "Alta"
        elif diff < -threshold:
            flutation = "Queda"
        else:
            flutation = "Manteve"

        return jsonify({
            "ticker": ticker,
            "actual_value": round(actual_value, 4),
            "prediction_value": round(prediction_value, 4),
            "variation_percent": round((diff / actual_value) * 100, 2),
            "flutation": flutation
        })

    except Exception as e:
        print(e)
        return jsonify({"error": "Erro interno no servidor."}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)