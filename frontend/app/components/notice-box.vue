<script setup lang="ts">
interface Props {
    message: string
}
defineProps<Props>()
</script>

<template>
    <div class="notice">
        <span class="icon">⚠️</span>
        <span class="text">{{ message }}</span>
    </div>
</template>

<style>
.notice {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 16px;
    padding: 8px 14px;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.03);
    font-size: 15px;
    line-height: 1.4;
    white-space: nowrap;
}

.icon {
    width: 16px;
    height: 16px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--warning);
}

.text {
    color: var(--fg);
}
</style>
