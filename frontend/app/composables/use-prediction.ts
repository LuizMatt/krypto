import { ref } from "vue"

export type PredictionResponse = {
    ticker: string
    actual_value: number
    prediction_value: number
    flutation: "Alta" | "Queda" | "Manteve" | string
}

export function usePrediction() {
    const data = ref<PredictionResponse | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function fetchPrediction() {
        loading.value = true
        error.value = null

        try {
            const config = useRuntimeConfig()

            const baseURL = (config.public.predictionsApiBase ??
                "http://localhost:5001") as string

            data.value = await $fetch<PredictionResponse>("/api/predict", {
                baseURL,
                method: "GET",
            })
        } catch (e: any) {
            console.error(e)
            error.value = e?.message ?? "Erro ao buscar previsão"
        } finally {
            loading.value = false
        }
    }

    return {
        data,
        loading,
        error,
        fetchPrediction,
    }
}
