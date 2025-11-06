<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from "vue"
import { useWatchlist, type SortKey } from "../composables/use-watch-list"
import { useCoingecko, type MarketRow } from "../composables/use-coingecko"

const { ids, q, sortBy, sortDir, toggle, setSort } = useWatchlist()
const { markets } = useCoingecko()

const loading = ref(false)
const error = ref<string | null>(null)
const rows = ref<MarketRow[]>([])

async function load() {
    if (!ids.value.length) { rows.value = []; return }
    try {
        loading.value = true
        error.value = null
        rows.value = await markets(ids.value)
    } catch (e: any) {
        error.value = e?.message ?? "Failed to fetch"
    } finally {
        loading.value = false
    }
}

let t: number | null = null
function startPolling(ms = 30000) {
    stopPolling()
    t = window.setInterval(() => {
        if (!document.hidden) load()
    }, ms)
}
function stopPolling() { if (t) { clearInterval(t); t = null } }

onMounted(() => { load(); startPolling(30000) })
onBeforeUnmount(stopPolling)

const filtered = computed(() => {
    const text = q.value.trim().toLowerCase()
    const list = rows.value.filter(r =>
        !text || r.name.toLowerCase().includes(text) || r.symbol.toLowerCase().includes(text)
    )
    const dir = sortDir.value === "asc" ? 1 : -1
    const key = sortBy.value as SortKey
    return list.sort((a, b) => {
        switch (key) {
            case "asset": return a.name.localeCompare(b.name) * dir
            case "price": return ((a.current_price ?? 0) - (b.current_price ?? 0)) * dir
            case "h1": return ((a.price_change_percentage_1h_in_currency ?? 0) - (b.price_change_percentage_1h_in_currency ?? 0)) * dir
            case "h24": return ((a.price_change_percentage_24h_in_currency ?? 0) - (b.price_change_percentage_24h_in_currency ?? 0)) * dir
            case "d7": return ((a.price_change_percentage_7d_in_currency ?? 0) - (b.price_change_percentage_7d_in_currency ?? 0)) * dir
            case "volume": return ((a.total_volume ?? 0) - (b.total_volume ?? 0)) * dir
        }
    })
})

function money(n: number) {
    return n.toLocaleString("en-US", { style: "currency", currency: "USD" })
}
function pct(n: number | null | undefined) {
    if (n == null) return "—"
    const sign = n > 0 ? "+" : ""
    return `${sign}${n.toFixed(2)}%`
}

function hasSpark(r: MarketRow): boolean {
    const s = r.sparkline_in_7d && r.sparkline_in_7d.price
    return Array.isArray(s) && s.length > 0
}
function sparkPointsFrom(r: MarketRow): string {
    const series = (r.sparkline_in_7d && r.sparkline_in_7d.price) || []
    if (series.length === 0) return ""
    const min = Math.min(...series)
    const max = Math.max(...series)
    const normY = (v: number) => (max === min ? 12 : 24 - ((v - min) / (max - min)) * 24)
    const N = series.length
    return series.map((v, i) => `${(i / (N - 1)) * 100},${normY(v)}`).join(" ")
}
function lastDelta(r: MarketRow): number {
    const s = r.sparkline_in_7d && r.sparkline_in_7d.price
    if (!s || s.length < 2) return 0
    const first = s[0] ?? 0
    const last = s[s.length - 1] ?? first
    return last - first
}
</script>

<template>
    <section class="card">
        <div class="header">
            <h2>Watchlist</h2>
            <input v-model="q" class="search" placeholder="Search watchlist..." />
        </div>

        <div v-if="!ids.length" class="empty">
            <p>Your watchlist is empty.</p>
            <NuxtLink to="/markets" class="btn">Go to Markets</NuxtLink>
        </div>

        <div v-else>
            <table class="tbl" aria-label="Watchlist table">
                <thead>
                    <tr>
                        <th class="w-asset" @click="setSort('asset')">
                            Asset <i class="sort" :class="[sortBy === 'asset' ? sortDir : '']"></i>
                        </th>
                        <th @click="setSort('price')">
                            Price <i class="sort" :class="[sortBy === 'price' ? sortDir : '']"></i>
                        </th>
                        <th @click="setSort('h1')">1h <i class="sort" :class="[sortBy === 'h1' ? sortDir : '']"></i>
                        </th>
                        <th @click="setSort('h24')">24h <i class="sort" :class="[sortBy === 'h24' ? sortDir : '']"></i>
                        </th>
                        <th @click="setSort('d7')">7d <i class="sort" :class="[sortBy === 'd7' ? sortDir : '']"></i>
                        </th>
                        <th>Sparkline</th>
                        <th @click="setSort('volume')">
                            Volume <i class="sort" :class="[sortBy === 'volume' ? sortDir : '']"></i>
                        </th>
                        <th></th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="r in filtered" :key="r.id">
                        <td class="asset">
                            <button class="star" :aria-label="'Toggle ' + r.name"
                                @click.prevent="toggle(r.id)">★</button>
                            <img :src="r.image" :alt="r.name" />
                            <div class="names">
                                <strong>{{ r.symbol.toUpperCase() }}</strong>
                                <small>{{ r.name }}</small>
                            </div>
                        </td>

                        <td class="num">{{ money(r.current_price) }}</td>

                        <td :class="['num', (r.price_change_percentage_1h_in_currency ?? 0) >= 0 ? 'pos' : 'neg']">
                            {{ pct(r.price_change_percentage_1h_in_currency) }}
                        </td>

                        <td :class="['num', (r.price_change_percentage_24h_in_currency ?? 0) >= 0 ? 'pos' : 'neg']">
                            {{ pct(r.price_change_percentage_24h_in_currency) }}
                        </td>

                        <td :class="['num', (r.price_change_percentage_7d_in_currency ?? 0) >= 0 ? 'pos' : 'neg']">
                            {{ pct(r.price_change_percentage_7d_in_currency) }}
                        </td>

                        <td class="spark">
                            <svg v-if="hasSpark(r)" viewBox="0 0 100 24" preserveAspectRatio="none">
                                <polyline :points="sparkPointsFrom(r)"
                                    :class="lastDelta(r) >= 0 ? 'line-pos' : 'line-neg'" />
                            </svg>
                        </td>

                        <td class="num">{{ money(r.total_volume) }}</td>

                        <td class="actions">
                            <NuxtLink :to="`/markets/${r.id}`" class="btn">View</NuxtLink>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div v-if="loading" class="footer muted">Updating…</div>
            <div v-if="error" class="footer error">Error: {{ error }}</div>
        </div>
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
    --tm-row-bg: #0f1420;
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

.header h2 {
    font-size: 1.1rem;
    font-weight: 700;
}

.search {
    width: 260px;
    background: var(--tm-bg);
    color: var(--tm-text);
    border: 1px solid var(--tm-border);
    border-radius: 10px;
    padding: 8px 10px;
    font-size: 14px;
    outline: none;
}

.tbl {
    width: 100%;
    border-collapse: collapse;
}

thead th {
    text-align: left;
    font-weight: 600;
    color: var(--tm-muted);
    padding: 10px;
    cursor: pointer;
    user-select: none;
    font-size: 14px;
}

tbody td {
    padding: 10px;
    border-top: 1px solid var(--tm-border);
    vertical-align: middle;
    font-size: 14px;
    background: var(--tm-row-bg);
}

tbody tr:hover td {
    background: rgba(255, 255, 255, 0.03);
}

.w-asset {
    width: 32%;
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
    color: #f4b400;
    font-size: 16px;
    cursor: pointer;
    margin-right: 4px;
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

.spark svg {
    width: 100px;
    height: 24px;
}

.line-pos {
    fill: none;
    stroke: var(--tm-green);
    stroke-width: 2;
}

.line-neg {
    fill: none;
    stroke: var(--tm-red);
    stroke-width: 2;
}

.actions .btn,
.btn {
    display: inline-block;
    padding: 5px 10px;
    border: 1px solid var(--tm-border);
    border-radius: 10px;
    color: var(--tm-text);
    background: var(--tm-bg);
    text-decoration: none;
    font-size: 13px;
}

.muted {
    color: var(--tm-muted);
}

.footer {
    margin-top: 8px;
    font-size: 12px;
    color: var(--tm-muted);
}

.error {
    color: var(--tm-red);
}

.empty {
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    color: var(--tm-muted);
}

.sort {
    border: solid var(--tm-muted);
    border-width: 0 2px 2px 0;
    display: inline-block;
    padding: 3px;
    margin-left: 6px;
    transform: rotate(-45deg);
    opacity: 0.4;
}

.sort.asc {
    transform: rotate(135deg);
    opacity: 1;
}

.sort.desc {
    transform: rotate(-45deg);
    opacity: 1;
}
</style>