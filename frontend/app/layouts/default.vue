<template>
    <div class="layout">
        <Navbar />

        <main class="container">
            <slot />
        </main>

        <Footer />
    </div>
</template>

<script setup>
</script>

<style>
:root {
    --header-height: 60px;
    --bg: #0b0e13;
    --fg: rgba(255, 255, 255, .87);
    --muted: #9aa3ad;
    --border: #1a2430;
    --warning: #f4b400;
    --heading-color: var(--fg);
}

.layout {
    background: var(--bg);
    color: var(--fg);
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
}

.container {
    padding-top: var(--header-height);
    padding-left: 24px;
    padding-right: 24px;
    max-width: 1100px;
    margin: 0 auto;
    flex: 1 0 auto;
    width: 100%;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: var(--heading-color);
}
</style>
