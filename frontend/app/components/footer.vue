<template>
    <footer class="footer">
        <div class="footer-inner">
            <div class="footer-brand">
                <span class="footer-logo-dot"></span>
                <div class="footer-brand-text">
                    <strong>Krypto AI</strong>
                    <span>Real-time crypto insights</span>
                </div>
            </div>

            <nav class="footer-links">
                <NuxtLink to="/">Overview</NuxtLink>
                <NuxtLink to="/markets">Markets</NuxtLink>
                <NuxtLink to="/predictions">Predictions</NuxtLink>
                <NuxtLink to="/about">About</NuxtLink>
            </nav>

            <div class="footer-note">
                <p>Academic project. Not financial or investment advice.</p>
                <p class="footer-meta">Market data sourced from public APIs.</p>
            </div>
        </div>
    </footer>
</template>

<style scoped>
.footer {
    border-top: 1px solid var(--border);
    padding: 18px 24px 22px;
    color: var(--muted);
    font-size: 13px;
    flex-shrink: 0;
    margin-top: 40px;
}

.footer-inner {
    max-width: 1100px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
}

.footer-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.footer-logo-dot {
    width: 20px;
    height: 20px;
    border-radius: 999px;
    background: var(--warning);
    box-shadow: 0 0 0 4px rgba(244, 180, 0, 0.16);
}

.footer-brand-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.footer-brand-text strong {
    font-size: 14px;
    letter-spacing: 0.02em;
}

.footer-brand-text span {
    font-size: 12px;
    color: var(--muted);
}

.footer-links {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.footer-links a {
    color: var(--muted);
    text-decoration: none;
    font-size: 13px;
    transition: color 0.15s ease, transform 0.15s ease;
}

.footer-links a:hover {
    color: var(--warning);
    transform: translateY(-1px);
}

.footer-note {
    text-align: right;
    max-width: 280px;
    line-height: 1.4;
}

.footer-meta {
    font-size: 11px;
    opacity: 0.8;
    margin-top: 2px;
}

@media (max-width: 768px) {
    .footer-note {
        text-align: left;
        max-width: 100%;
    }
}
</style>
