<script setup lang="ts">
import {useCryptoTicker} from "../composables/use-crypto-ticker"

const { items, loading, error } = useCryptoTicker(["BTC", "ETH", "XRP", "ADA", "SOL"])
</script>

<template>
    <section class="page">
        <home-hero title="Market Overview" subtitle="Real-time cryptocurrency prices and AI-powered predictions!" />
        <notice-box message="This is not investment advice. All predictions are for informational purposes only." />

        <crypto-ticker v-if="!loading && !error" :items="items" />
        <div v-if="loading" class="status">Loading prices...</div>
        <div v-if="error" class="status error">{{ error }}</div>

        <top-movers />
        <watchlist-table />
    </section>
</template>

<style scoped>
.page {
    display: flex;
    flex-direction: column;
    gap: 24px;
    padding: 16px 0;
}

.status {
    text-align: center;
    color: #9aa3ad;
    font-size: 0.9rem;
}

.status.error {
    color: #ef4444;
}
</style>
