<template>
    <section class="about-grid">
        <article class="card">
            <h2>What is this project?</h2>
            <p>
                Krypto AI is a study project focused on cryptocurrency markets. The goal
                is to practice frontend development, API integration and data
                visualization using real-time market data.
            </p>
            <p>
                The interface simulates a professional dashboard, but all features are
                designed for learning and experimentation only.
            </p>
        </article>

        <article class="card">
            <h2>How do the predictions work?</h2>
            <p>
                The Bitcoin prediction module uses an LSTM-based model trained on
                historical price data. The backend exposes a simple API that returns the
                last known value and the next predicted value.
            </p>
            <p class="muted">
                The model is intentionally simplified and does not try to beat the
                market. It exists only to demonstrate how AI can be integrated into a
                web application.
            </p>
        </article>

        <article class="card">
            <h2>Tech stack</h2>
            <ul class="list">
                <li><strong>Frontend:</strong> Nuxt 3, Vue 3, Composition API</li>
                <li><strong>Styling:</strong> Custom CSS with a dark, dashboard-style UI</li>
                <li><strong>Data:</strong> Public cryptocurrency APIs for market prices</li>
                <li><strong>AI / ML:</strong> LSTM model running on a small Python backend</li>
            </ul>
        </article>

        <article class="card">
            <h2>Goals and learning</h2>
            <p>
                This project was built to practice component-based design, state
                management with composables, API consumption and UX focused on data
                dashboards.
            </p>
            <p>
                It also serves as a portfolio piece to demonstrate knowledge of modern
                web development and basic machine learning integration.
            </p>
        </article>
    </section>
</template>

<style scoped>
.about-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 18px;
    margin-top: 8px;
}

.card {
    background: #111827;
    border-radius: 16px;
    padding: 18px 18px 16px;
    border: 1px solid #1f2937;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
}

.card h2 {
    font-size: 1rem;
    margin-bottom: 8px;
}

.card p {
    font-size: 0.9rem;
    color: var(--fg);
    margin-bottom: 6px;
}

.card p:last-child {
    margin-bottom: 0;
}

.muted {
    color: var(--muted);
}

.list {
    list-style: none;
    padding: 0;
    margin: 6px 0 0;
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 0.9rem;
    color: var(--fg);
}

.list strong {
    font-weight: 600;
}
</style>
