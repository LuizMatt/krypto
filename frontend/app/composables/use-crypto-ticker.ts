import { ref, onMounted, onBeforeUnmount } from "vue"

const ID_MAP: Record<string, string> = {
  BTC: "bitcoin",
  ETH: "ethereum",
  XRP: "ripple",
  ADA: "cardano",
  SOL: "solana",
}

export type TickerItem = {
  symbol: string
  price: number
  changePct: number
}

export function useCryptoTicker(symbols: string[] = ["BTC", "XRP", "ADA"], refreshMs = 60_000) {
  const items = ref<TickerItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  let timer: number | undefined

  const ids = symbols
    .map(s => ID_MAP[s.toUpperCase()] ?? s.toLowerCase())
    .join(",")

  const fetchNow = async () => {
    loading.value = true
    error.value = null
    try {
      const data = await $fetch<any[]>("https://api.coingecko.com/api/v3/coins/markets", {
        query: {
          vs_currency: "usd",
          ids,
          // sem sparkline:
          sparkline: "false",
          price_change_percentage: "24h",
        },
      })

      items.value = (data ?? []).map((r: any) => ({
        symbol: String(r.symbol ?? "").toUpperCase(),
        price: Number(r.current_price ?? 0),
        changePct: Number(
          r.price_change_percentage_24h_in_currency ?? r.price_change_percentage_24h ?? 0
        ),
      }))
    } catch (e: any) {
      error.value = e?.message ?? "Erro ao buscar dados"
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
    fetchNow()
    timer = window.setInterval(fetchNow, refreshMs)
  })
  onBeforeUnmount(() => {
    if (timer) clearInterval(timer)
  })

  return { items, loading, error, fetchNow }
}
