type CacheEntry = {
    time: number
    data: any
}

const cache = new Map<string, CacheEntry>()
const TTL = 120_000 

export default defineEventHandler(async (event) => {
    const query = getQuery(event)

    const url = "https://api.coingecko.com/api/v3/coins/markets"

    const key = JSON.stringify(query)
    const now = Date.now()

    const cached = cache.get(key)
    if (cached && now - cached.time < TTL) {
        return cached.data
    }

    try {
        const data = await $fetch(url, { query })

        cache.set(key, { time: now, data })

        return data
    } catch (err) {
        if (cached) {
            return cached.data
        }
        throw err
    }
})
