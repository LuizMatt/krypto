import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import yfinance as yf
import mwclient
import time
import os
import pickle

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential
from transformers import pipeline
from statistics import mean

# CONFIGURAÇÕES GERAIS
CRYPTO_CURRENCY = 'BTC'
AGAINST_CURRENCY = 'USD'
TICKER = f"{CRYPTO_CURRENCY}-{AGAINST_CURRENCY}"
PREDICTION_DAYS = 60
WIKI_PAGE = "Bitcoin"

#AQUISIÇÃO E ANÁLISE DE SENTIMENTO (WIKIPEDIA)
def get_wiki_data():
    """
    Busca edições da Wikipedia, aplica análise de sentimento e salva em CSV.
    Se o CSV já existir, carrega dele para economizar tempo.
    """
    if os.path.exists("wikipedia_edits.csv"):
        print("=> Carregando dados da Wikipedia do arquivo local (cache)...")
        return pd.read_csv("wikipedia_edits.csv", index_col=0, parse_dates=True)

    print("=> Baixando dados da Wikipedia (isso pode demorar)...")
    site = mwclient.Site("en.wikipedia.org")
    page = site.pages[WIKI_PAGE]
    
    revs = []
    try:
        revisions = page.revisions()
        for i, rev in enumerate(revisions):
            revs.append(rev)
            if i % 100 == 0: print(f"Baixadas {i} revisões...")
            if i >= 2000: break
    except Exception as e:
        print(f"Erro ao baixar revisões: {e}")

    print(f"=> Aplicando Análise de Sentimento em {len(revs)} revisões...")
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def find_sentiment(text):
        try:
            sent = sentiment_pipeline([text[:512]])[0]
            score = sent["score"]
            if sent["label"] == "NEGATIVE":
                score *= -1
            return score
        except:
            return 0

    edits = {}
    for rev in revs:
        date = time.strftime("%Y-%m-%d", rev["timestamp"])
        
        if date not in edits:
            edits[date] = dict(sentiments=list(), edit_count=0)
        
        edits[date]["edit_count"] += 1
        
        comment = rev.get("comment", "")
        edits[date]["sentiments"].append(find_sentiment(comment))

    for key in edits:
        if len(edits[key]["sentiments"]) > 0:
            edits[key]["sentiment_mean"] = mean(edits[key]["sentiments"])
            neg_sents = [s for s in edits[key]["sentiments"] if s < 0]
            edits[key]["neg_sentiment_ratio"] = len(neg_sents) / len(edits[key]["sentiments"])
        else:
            edits[key]["sentiment_mean"] = 0
            edits[key]["neg_sentiment_ratio"] = 0
        
        del edits[key]["sentiments"]

    edits_df = pd.DataFrame.from_dict(edits, orient="index")
    edits_df.index = pd.to_datetime(edits_df.index)
    
    dates = pd.date_range(start=edits_df.index.min(), end=dt.datetime.today())
    edits_df = edits_df.reindex(dates, fill_value=0)
    
    rolling_edits = edits_df.rolling(30, min_periods=1).mean()
    
    rolling_edits.to_csv(f"wikipedia_edits_{CRYPTO_CURRENCY}.csv")
    return rolling_edits


# PREPARAÇÃO DOS DADOS

print("=> Baixando dados financeiros do Yahoo Finance...")
start = dt.datetime(2018, 1, 1)
end = dt.datetime.now()
btc_data = yf.download(TICKER, start, end)

if isinstance(btc_data.columns, pd.MultiIndex):
    btc_data.columns = btc_data.columns.get_level_values(0)

if 'Adj Close' in btc_data.columns:
    btc_data = btc_data.drop(columns=['Adj Close'])
btc_data.columns = [c.lower() for c in btc_data.columns]

wiki_data = get_wiki_data()

print("=> Unificando datasets...")
merged_data = btc_data.merge(wiki_data, left_index=True, right_index=True, how='inner')

merged_data = merged_data.dropna()

print(f"Dataset Final Shape: {merged_data.shape}")
print("Colunas usadas:", merged_data.columns)

# PREPARAÇÃO (SCALING)

feature_columns = ['close', 'volume', 'edit_count', 'sentiment_mean', 'neg_sentiment_ratio']
target_column = 'close' 

scaler_features = MinMaxScaler(feature_range=(0, 1))
scaler_target = MinMaxScaler(feature_range=(0, 1))

scaled_data = scaler_features.fit_transform(merged_data[feature_columns].values)
scaler_target.fit(merged_data[[target_column]].values)

x_train, y_train = [], []

train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size - PREDICTION_DAYS:]

for x in range(PREDICTION_DAYS, len(train_data)):
    x_train.append(train_data[x-PREDICTION_DAYS:x])
    y_train.append(train_data[x, 0]) 

x_train, y_train = np.array(x_train), np.array(y_train)

# CONSTRUÇÃO E TREINO

print("=> Construindo Modelo LSTM Multivariado...")
model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')

print("=> Treinando...")
model.fit(x_train, y_train, epochs=25, batch_size=32)

# TESTE E PREVISÃO

x_test = []
actual_prices = merged_data[target_column].values[train_size:]

for x in range(PREDICTION_DAYS, len(test_data)):
    x_test.append(test_data[x-PREDICTION_DAYS:x])

x_test = np.array(x_test)

predicted_prices_scaled = model.predict(x_test)
predicted_prices = scaler_target.inverse_transform(predicted_prices_scaled)

# VISUALIZAÇÃO E SALVAMENTO

plt.figure(figsize=(10,5))
plt.plot(actual_prices, color='black', label="Preço Real")
plt.plot(predicted_prices, color='green', label="Preço Previsto (Com Sentimento)")
plt.title(f'{CRYPTO_CURRENCY} Price Prediction')
plt.xlabel('Tempo')
plt.ylabel('Preço')
plt.legend(loc='upper left')
plt.show()

real_data = [test_data[len(test_data) - PREDICTION_DAYS:len(test_data)]]
real_data = np.array(real_data)
prediction_scaled = model.predict(real_data)
prediction = scaler_target.inverse_transform(prediction_scaled)

print(f"\n==================================================")
print(f"Previsão de PREÇO para amanhã: {prediction[0][0]:.2f} USD")
print(f"==================================================")

model.save(f"{CRYPTO_CURRENCY}_model")
with open(f"scaler_{CRYPTO_CURRENCY}_features.pkl", "wb") as f:
    pickle.dump(scaler_features, f)
with open(f"scaler_{CRYPTO_CURRENCY}_target.pkl", "wb") as f:
    pickle.dump(scaler_target, f)

print("Modelos e Scalers salvos com sucesso.")