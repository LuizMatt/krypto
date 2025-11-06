<script setup lang="ts">
import { computed, ref, onMounted, nextTick } from "vue"

type TickerItem = {
    symbol: string
    price: number
    changePct: number
}

const props = defineProps<{
    items: TickerItem[]
}>()

const container = ref<HTMLElement | null>(null)
const track = ref<HTMLElement | null>(null)

const loopItems = computed(() => [...props.items, ...props.items])

const duration = ref(20)
const loopDistance = ref(0)

function money(n: number) {
    return n.toLocaleString("en-US", { style: "currency", currency: "USD" })
}

onMounted(async () => {
    await nextTick()
    if (!container.value || !track.value) return
    const half = track.value.scrollWidth / 2
    loopDistance.value = half
    const pxPerSec = 80
    duration.value = Math.max(10, Math.round(half / pxPerSec))
})
</script>

<template>
    <div ref="container" class="ticker scroller">
        <div ref="track" class="track"
            :style="{ '--duration': duration + 's', '--loop-distance': loopDistance + 'px' }">
            <div v-for="(it, i) in loopItems" :key="i" class="pill">
                <div class="meta">
                    <span class="sym">{{ it.symbol }}</span>
                    <span class="price">{{ money(it.price) }}</span>
                    <span class="chg" :class="it.changePct >= 0 ? 'up' : 'down'">
                        <svg viewBox="0 0 10 10" class="arrow" aria-hidden="true">
                            <path v-if="it.changePct >= 0" d="M1 6 L5 2 L9 6" />
                            <path v-else d="M1 4 L5 8 L9 4" />
                        </svg>
                        {{ it.changePct.toFixed(2) }}%
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.ticker {
    --bg: #0c1118;
    --pill: #121824;
    --text: #e6eaf2;
    --border: #1f2937;
    --up: #2ecc71;
    --down: #ef4444;
}

.scroller {
    position: relative;
    overflow: hidden;
    background: var(--bg);
    border-radius: 8px;
    padding: 8px;
}

.track {
    display: inline-flex;
    gap: 14px;
    will-change: transform;
    animation: scroll var(--duration) linear infinite;
}

.scroller:hover .track {
    animation-play-state: paused;
}

@media (prefers-reduced-motion: reduce) {
    .track {
        animation: none;
    }
}

@keyframes scroll {
    from {
        transform: translateX(0);
    }

    to {
        transform: translateX(calc(-1 * var(--loop-distance)));
    }
}

.pill {
    display: flex;
    align-items: center;
    gap: 14px;
    background: var(--pill);
    padding: 10px 14px;
    border-radius: 14px;
    border: 1px solid var(--border);
}

.meta {
    display: flex;
    align-items: center;
    gap: 10px;
}

.sym {
    font-weight: 800;
    letter-spacing: 0.5px;
    color: var(--text);
}

.price {
    color: var(--text);
    opacity: 0.9;
    font-variant-numeric: tabular-nums;
}

.chg {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-variant-numeric: tabular-nums;
    color: var(--down);
}

.chg.up {
    color: var(--up);
}

.chg.down {
    color: var(--down);
}

.arrow {
    width: 10px;
    height: 10px;
    fill: none;
    stroke: currentColor;
    stroke-width: 1.5;
}
</style>
