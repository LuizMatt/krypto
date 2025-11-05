<script setup lang="ts">
interface Props {
    title: string
    subtitle?: string
}
defineProps<Props>()
</script>

<template>
    <header class="section-header">
        <h1 class="title">{{ title }}</h1>
        <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    </header>
</template>

<style>
.section-header {
    margin: 24px 0 16px;
}

.title {
    margin: 0 0 6px;
    font-size: 32px;
    line-height: 1.2;
    font-weight: 700;
}

.subtitle {
    margin: 0;
    font-size: 16px;
    color: var(--muted);
}

@media (min-width: 768px) {
    .title {
        font-size: 36px;
    }
}
</style>
