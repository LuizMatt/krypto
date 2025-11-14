<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { useCoingecko, type MarketRow } from "../../composables/use-coingecko"
import { useWatchlist } from "../../composables/use-watch-list"

const MARKET_IDS = [
    "bitcoin",
    "ethereum",
    "tether",
    "binancecoin",
    "solana",
    "ripple",
    "cardano",
    "dogecoin",
    "tron",
    "litecoin",
]

const { markets } = useCoingecko()
const { ids: favIds, toggle } = useWatchlist()

const loading = ref(false)
const error = ref<string | null>(null)
const rows = ref<MarketRow[]>([])
const q = ref("")

async function load() {
    try {
        loading.value = true
        error.value = null
        rows.value = await markets(MARKET_IDS)
    } catch (e: any) {
        error.value = e?.message ?? "Failed to fetch markets"
    } finally {
        loading.value = false
    }
}

onMounted(load)

const filtered = computed(() => {
    const text = q.value.trim().toLowerCase()
    return rows.value.filter(r =>
        !text ||
        r.name.toLowerCase().includes(text) ||
        r.symbol.toLowerCase().includes(text)
    )
})

function isFav(id: string) {
    return favIds.value.includes(id)
}

function money(n: number) {
    return n.toLocaleString("en-US", { style: "currency", currency: "USD" })
}
</script>

<template>
    <section class="card">
        <div class="header">
            <div>
                <h1>Markets</h1>
                <p class="subtitle">
                    Browse coins and add them to your watchlist.
                </p>
            </div>

            <input v-model="q" class="search" placeholder="Search by name or symbol..." />
        </div>

        <div v-if="loading" class="state">Loading markets…</div>
        <div v-else-if="error" class="state error">Error: {{ error }}</div>

        <table v-else class="tbl" aria-label="Markets table">
            <thead>
                <tr>
                    <th class="w-asset">Asset</th>
                    <th class="th-num">Price</th>
                    <th class="th-num">24h %</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="r in filtered" :key="r.id">
                    <td class="asset">
                        <button class="star" :class="{ active: isFav(r.id) }"
                            :aria-label="'Toggle ' + r.name + ' in watchlist'" @click.prevent="toggle(r.id)">
                            {{ isFav(r.id) ? "★" : "☆" }}
                        </button>

                        <img :src="r.image" :alt="r.name" />

                        <div class="names">
                            <strong>{{ r.symbol.toUpperCase() }}</strong>
                            <small>{{ r.name }}</small>
                        </div>
                    </td>

                    <td class="num">{{ money(r.current_price) }}</td>

                    <td class="num" :class="(r.price_change_percentage_24h_in_currency ?? 0) >= 0 ? 'pos' : 'neg'">
                        {{
                            r.price_change_percentage_24h_in_currency == null
                                ? "—"
                                : r.price_change_percentage_24h_in_currency.toFixed(2) + '%'
                        }}
                    </td>
                </tr>
            </tbody>
        </table>
    </section>
</template>

<style scoped>
.card {
    --tm-bg: #0b0e13;
    --tm-text: #e6eaf2;
    --tm-muted: #9aa4b2;
    --tm-border: #1f2937;
    --tm-green: #16a34a;
    --tm-red: #dc2626;
    --tm-panel-bg: #101623;
    background: var(--tm-panel-bg);
    border: 1px solid var(--tm-border);
    border-radius: 14px;
    padding: 20px;
    color: var(--tm-text);
    margin-top: 24px;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.header h1 {
    font-size: 1.4rem;
    font-weight: 700;
}

.subtitle {
    font-size: 0.9rem;
    color: var(--tm-muted);
}

.search {
    width: 260px;
    max-width: 40vw;
    background: var(--tm-bg);
    color: var(--tm-text);
    border: 1px solid var(--tm-border);
    border-radius: 10px;
    padding: 8px 10px;
    font-size: 14px;
    outline: none;
}

.search::placeholder {
    color: var(--tm-muted);
}

.tbl {
    width: 100%;
    border-collapse: collapse;
}

thead th {
    font-weight: 600;
    color: var(--tm-muted);
    padding: 10px;
    font-size: 14px;
}
.th-num {
    text-align: right;
}

.w-asset {
    width: 55%;
}

tbody td {
    padding: 10px;
    border-top: 1px solid var(--tm-border);
    vertical-align: middle;
    font-size: 14px;
    background: #0f1420;
}

tbody tr:hover td {
    background: rgba(255, 255, 255, 0.03);
}

.asset {
    display: flex;
    align-items: center;
    gap: 10px;
}

.asset img {
    width: 24px;
    height: 24px;
    border-radius: 50%;
}

.asset .names {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
}

.star {
    background: transparent;
    border: 0;
    font-size: 18px;
    cursor: pointer;
    margin-right: 6px;
    color: var(--tm-muted);
}

.star.active {
    color: #f4b400;
}

.num {
    text-align: right;
    font-variant-numeric: tabular-nums;
}

.pos {
    color: var(--tm-green);
}

.neg {
    color: var(--tm-red);
}

.state {
    padding: 16px 0;
    font-size: 14px;
    color: var(--tm-muted);
}

.state.error {
    color: var(--tm-red);
}
</style>
