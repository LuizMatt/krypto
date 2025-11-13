import { computed } from "vue"

export type MarketRow = {
  id: string
  symbol: string
  name: string
  image: string
  current_price: number
  total_volume: number
  price_change_percentage_1h_in_currency: number | null
  price_change_percentage_24h_in_currency: number | null
  price_change_percentage_7d_in_currency: number | null
  sparkline_in_7d?: { price: number[] }
}

const BASE = "/api/coingecko"

export function useCoingecko() {
  async function markets(ids: string[]) {
    if (!ids.length) return []

    return await $fetch<MarketRow[]>(`${BASE}/markets`, {
      query: {
        vs_currency: "usd",
        ids: ids.join(","),
        order: "market_cap_desc",
        per_page: ids.length,
        page: 1,
        price_change_percentage: "1h,24h,7d",
        sparkline: true,
      },
    })
  }

  return { markets }
}