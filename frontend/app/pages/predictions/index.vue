<script setup lang="ts">
import { onMounted } from "vue"
import { usePrediction } from "../../composables/use-prediction"

const { data, loading, error, fetchPrediction } = usePrediction()

onMounted(() => {
    fetchPrediction()
})

function formatUsd(value?: number) {
    if (value == null) return "-"
    return value.toLocaleString("en-US", {
        style: "currency",
        currency: "USD",
    })
}
</script>

<template>
    <section class="page">
        <home-hero title="BTC Predictions" subtitle="LSTM-based prediction for the next Bitcoin move." />

        <notice-box
            message="These predictions are experimental and for educational purposes only. Not financial advice." />

        <div class="prediction-card">
            <header class="prediction-header">
                <h2>Bitcoin price prediction</h2>
                <button class="refresh-btn" type="button" @click="fetchPrediction" :disabled="loading">
                    {{ loading ? "Atualizando..." : "Atualizar previsão" }}
                </button>
            </header>

            <p v-if="error" class="status error">
                {{ error }}
            </p>

            <div v-else-if="!data && loading" class="status">
                Carregando previsão...
            </div>

            <div v-else-if="data" class="prediction-grid">
                <div class="prediction-item">
                    <span class="label">Ticker</span>
                    <span class="value">{{ data.ticker }}</span>
                </div>

                <div class="prediction-item">
                    <span class="label">Preço atual</span>
                    <span class="value">{{ formatUsd(data.actual_value) }}</span>
                </div>

                <div class="prediction-item">
                    <span class="label">Preço previsto</span>
                    <span class="value">{{ formatUsd(data.prediction_value) }}</span>
                </div>

                <div class="prediction-item">
                    <span class="label">Tendência</span>
                    <span class="value badge" :class="{
                        up: data.flutation === 'Alta',
                        down: data.flutation === 'Queda',
                        flat: data.flutation === 'Manteve',
                    }">
                        {{ data.flutation }}
                    </span>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
.page {
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding: 16px 0 32px;
}

.prediction-card {
    background: #111827;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #1f2937;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.45);
}

.prediction-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.prediction-header h2 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f9fafb;
}

.refresh-btn {
    background: #22c55e;
    border: none;
    border-radius: 999px;
    padding: 8px 16px;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    color: #0b0e13;
    transition: background 0.15s ease, transform 0.1s ease;
}

.refresh-btn:hover:not(:disabled) {
    background: #16a34a;
    transform: translateY(-1px);
}

.refresh-btn:disabled {
    opacity: 0.6;
    cursor: default;
}

.status {
    text-align: center;
    font-size: 0.9rem;
    color: #9aa3ad;
}

.status.error {
    color: #ef4444;
}

.prediction-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-top: 8px;
}

.prediction-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.label {
    font-size: 0.8rem;
    color: #9aa3ad;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.value {
    font-size: 1rem;
    color: #e5e7eb;
    font-weight: 500;
}

.badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.8rem;
}

.badge.up {
    background: rgba(34, 197, 94, 0.12);
    color: #22c55e;
}

.badge.down {
    background: rgba(239, 68, 68, 0.12);
    color: #ef4444;
}

.badge.flat {
    background: rgba(148, 163, 184, 0.12);
    color: #e5e7eb;
}
</style>
