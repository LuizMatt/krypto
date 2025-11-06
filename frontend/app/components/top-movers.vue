<script setup lang="ts">
import { computed } from "vue"
import { useTopMovers } from "../composables/use-top-movers"

const props = withDefaults(defineProps<{
    symbols?: string[]
    gainersCount?: number
    losersCount?: number
    refreshMs?: number
    titleGainers?: string
    titleLosers?: string
}>(), {
    gainersCount: 5,
    losersCount: 5,
    refreshMs: 60000,
    titleGainers: "Top Gainers",
    titleLosers: "Top Losers",
})

const { gainers, losers, loading, error } = useTopMovers({
    symbols: props.symbols,
    gainersCount: props.gainersCount,
    losersCount: props.losersCount,
    refreshMs: props.refreshMs,
})

function money(n: number) {
    return n.toLocaleString("en-US", {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 2
    })
}

const hasData = computed(() => (gainers.value.length + losers.value.length) > 0)
</script>

<template>
    <div class="top-movers">
        <div class="grid">
            <section class="panel panel--gainers">
                <header class="panel-header">
                    <svg viewBox="0 0 10 10" class="arrow" aria-hidden="true">
                        <path d="M1 6 L5 2 L9 6" />
                    </svg>
                    <h3 class="panel-title">{{ props.titleGainers }}</h3>
                </header>

                <div v-if="loading && !hasData" class="state muted">Loading...</div>
                <div v-else-if="error && !hasData" class="state error">{{ error }}</div>

                <ul v-if="gainers.length" class="list">
                    <li v-for="it in gainers" :key="it.id" class="row row--up">
                        <div class="left">
                            <div class="sym">{{ it.symbol }}</div>
                            <div class="name">{{ it.name }}</div>
                        </div>
                        <div class="right">
                            <div class="pct">+{{ it.changePct.toFixed(2) }}%</div>
                            <div class="price">{{ money(it.price) }}</div>
                        </div>
                    </li>
                </ul>
            </section>

            <section class="panel panel--losers">
                <header class="panel-header">
                    <svg viewBox="0 0 10 10" class="arrow" aria-hidden="true">
                        <path d="M1 4 L5 8 L9 4" />
                    </svg>
                    <h3 class="panel-title">{{ props.titleLosers }}</h3>
                </header>

                <div v-if="loading && !hasData" class="state muted">Loading...</div>
                <div v-else-if="error && !hasData" class="state error">{{ error }}</div>

                <ul v-if="losers.length" class="list">
                    <li v-for="it in losers" :key="it.id" class="row row--down">
                        <div class="left">
                            <div class="sym">{{ it.symbol }}</div>
                            <div class="name">{{ it.name }}</div>
                        </div>
                        <div class="right">
                            <div class="pct">{{ it.changePct.toFixed(2) }}%</div>
                            <div class="price">{{ money(it.price) }}</div>
                        </div>
                    </li>
                </ul>
            </section>
        </div>
    </div>
</template>

<style scoped>
.top-movers {
    --tm-bg: #0b0e13;
    --tm-text: #e6eaf2;
    --tm-muted: #9aa4b2;
    --tm-border: #1f2937;
    --tm-green: #16a34a;
    --tm-green-bg: rgba(22, 163, 74, 0.1);
    --tm-red: #dc2626;
    --tm-red-bg: rgba(220, 38, 38, 0.1);
    --tm-panel-bg: #101623;
    --tm-row-bg: #0f1420;
    color: var(--tm-text);
}

.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.panel {
    background: var(--tm-panel-bg);
    border-radius: 14px;
    border: 1px solid var(--tm-border);
    padding: 16px;
}

.panel-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 14px;
    font-weight: 700;
    font-size: 1.1rem;
}

.panel--gainers .panel-header {
    color: var(--tm-green);
}

.panel--losers .panel-header {
    color: var(--tm-red);
}

.panel-title {
    line-height: 1.2;
}

.arrow {
    width: 16px;
    height: 16px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
}

.list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid var(--tm-border);
    background: var(--tm-row-bg);
    transition: background 0.2s ease;
}

.row--up {
    background: var(--tm-green-bg);
    border-color: rgba(22, 163, 74, 0.3);
}

.row--up:hover {
    background: rgba(22, 163, 74, 0.2);
}

.row--down {
    background: var(--tm-red-bg);
    border-color: rgba(220, 38, 38, 0.3);
}

.row--down:hover {
    background: rgba(220, 38, 38, 0.2);
}

.left {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.sym {
    font-weight: 800;
    letter-spacing: 0.5px;
}

.name {
    color: var(--tm-muted);
    font-size: 0.9rem;
}

.right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 3px;
}

.pct {
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}

.row--up .pct {
    color: var(--tm-green);
}

.row--down .pct {
    color: var(--tm-red);
}

.price {
    color: var(--tm-muted);
    font-variant-numeric: tabular-nums;
}

.state {
    padding: 12px;
    text-align: center;
    border-radius: 8px;
    border: 1px dashed var(--tm-border);
    margin-top: 8px;
}

.state.muted {
    color: var(--tm-muted);
}

.state.error {
    color: var(--tm-red);
}

@media (max-width: 900px) {
    .grid {
        grid-template-columns: 1fr;
    }
}
</style>