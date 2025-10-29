## Krypto Backend

Este backend em **Flask + TensorFlow** realiza previsões do preço do **Bitcoin (BTC-USD)** utilizando um modelo **LSTM** treinado e um **scaler** serializado.

---

## 🚀 Tecnologias
- Python 3.10+
- Flask
- TensorFlow / Keras
- Scikit-learn
- yFinance
- Flask-CORS

## 🧠 Rota principal

### `GET /api/predict`
Realiza a previsão do preço do Bitcoin para o próximo dia.

**Processo:**
1. Busca dados recentes do BTC-USD via **yFinance**.  
2. Usa os últimos **60 dias** como entrada do modelo LSTM.  
3. Retorna preço atual, preço previsto e tendência (Alta, Queda ou Manteve).

**Exemplo de resposta:**
```json
{
  "ticker": "BTC-USD",
  "actual_value": 68912.23,
  "prediction_value": 69234.11,
  "flutation": "Alta"
}
