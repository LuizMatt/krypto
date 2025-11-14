<template>
    <section class="about-hero">
        <div class="badge">About</div>
        <h1>Krypto AI</h1>
        <p class="subtitle">
            An academic project that combines real-time cryptocurrency data with
            machine learning experimentation to explore price predictions.
        </p>
    </section>
</template>

<style scoped>
.about-hero {
    padding: 24px 0 8px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: rgba(250, 204, 21, 0.1);
    color: var(--warning);
    border: 1px solid rgba(250, 204, 21, 0.4);
    width: fit-content;
}

h1 {
    font-size: 2rem;
    line-height: 1.1;
}

.subtitle {
    max-width: 640px;
    font-size: 0.95rem;
    color: var(--muted);
}
</style>
