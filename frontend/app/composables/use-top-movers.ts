import { ref, onMounted, onBeforeUnmount } from "vue"

export type CoinRow = {
  id: string
  symbol: string
  name: string
  price: number
  changePct: number
}

export function useTopMovers(opts?: {
  symbols?: string[]
  gainersCount?: number
  losersCount?: number
  refreshMs?: number
}) {
  const gainersCount = opts?.gainersCount ?? 5
  const losersCount = opts?.losersCount ?? 5
  const refreshMs = opts?.refreshMs ?? 60_000

  const gainers = ref<CoinRow[]>([])
  const losers = ref<CoinRow[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  let timer: number | undefined

  const fetchNow = async () => {
    loading.value = true
    error.value = null
    try {
      const base = "https://api.coingecko.com/api/v3/coins/markets"
      const query: Record<string, any> = {
        vs_currency: "usd",
        order: "market_cap_desc",
        per_page: 100,
        page: 1,
        sparkline: "false",
        price_change_percentage: "24h",
      }

      const data = await $fetch<any[]>(base, { query })

      let rows: CoinRow[] = (data ?? []).map((r) => ({
        id: String(r.id ?? ""),
        symbol: String(r.symbol ?? "").toUpperCase(),
        name: String(r.name ?? ""),
        price: Number(r.current_price ?? 0),
        changePct: Number(r.price_change_percentage_24h_in_currency ?? r.price_change_percentage_24h ?? 0),
      }))

      if (opts?.symbols?.length) {
        const set = new Set(opts.symbols.map((s) => s.toUpperCase()))
        rows = rows.filter((r) => set.has(r.symbol))
      }

      const up = rows.filter((r) => Number.isFinite(r.changePct) && r.changePct > 0)
        .sort((a, b) => b.changePct - a.changePct)
        .slice(0, gainersCount)

      const down = rows.filter((r) => Number.isFinite(r.changePct) && r.changePct < 0)
        .sort((a, b) => a.changePct - b.changePct)
        .slice(0, losersCount)

      gainers.value = up
      losers.value = down
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

  return { gainers, losers, loading, error, fetchNow }
}
