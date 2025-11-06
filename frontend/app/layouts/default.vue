<template>
    <div class="layout">
        <Navbar />
        <main class="container">
            <slot />
        </main>
    </div>
</template>

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
}

.container {
    padding-top: var(--header-height);
    padding-left: 24px;
    padding-right: 24px;
    max-width: 1100px;
    margin: 0 auto;
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
