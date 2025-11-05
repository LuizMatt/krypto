<template>
    <nav class="navbar" aria-label="Main navigation">
        <NuxtLink to="/" class="logo">
            <div class="logo-icon">
                <TrendingUp />
            </div>
            <span class="logo-text">Krypto AI</span>
        </NuxtLink>

        <ul class="nav-list">
            <li>
                <NuxtLink to="/overview" class="nav-link">
                    <TrendingUp class="icon" /> Overview
                </NuxtLink>
            </li>
            <li>
                <NuxtLink to="/markets" class="nav-link">
                    <BarChart3 class="icon" /> Markets
                </NuxtLink>
            </li>
            <li>
                <NuxtLink to="/predictions" class="nav-link">
                    <Target class="icon" /> Predictions
                </NuxtLink>
            </li>
            <li>
                <NuxtLink to="/settings" class="nav-link">
                    <Settings class="icon" /> Settings
                </NuxtLink>
            </li>
            <li>
                <NuxtLink to="/about" class="nav-link">
                    <Info class="icon" /> About
                </NuxtLink>
            </li>
        </ul>
    </nav>
</template>

<script setup>
import { TrendingUp, BarChart3, Target, Settings, Info } from 'lucide-vue-next'
</script>

<style scoped>
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    padding: 0 32px;
    background: rgba(11, 14, 19, 0.85);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid #1f2937;
    color: #fff;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
}

.logo-icon {
    background-color: #22d3ee;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: #0b0e13;
}

.logo-text {
    font-weight: 600;
    font-size: 18px;
    color: #22d3ee;
}

.nav-list {
    display: flex;
    align-items: center;
    gap: 20px;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #e5e7eb;
    text-decoration: none;
    font-weight: 500;
    font-size: 14px;
    border-radius: 9999px;
    padding: 8px 14px;
    transition: all 0.2s ease;
}

.nav-link:hover {
    background-color: rgba(255, 255, 255, 0.08);
}

.nav-link.router-link-active {
    background-color: #22d3ee;
    color: #0b0e13;
    font-weight: 600;
}

.icon {
    width: 16px;
    height: 16px;
    stroke-width: 2;
}

@media (max-width: 768px) {
    .navbar {
        padding: 0 16px;
    }

    .nav-list {
        gap: 12px;
    }
}
</style>
