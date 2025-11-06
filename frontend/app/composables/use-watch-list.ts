// composables/useWatchlist.ts
import { ref, type Ref } from "vue"

export type Id = string
export type SortKey = "asset" | "price" | "h1" | "h24" | "d7" | "volume"
export type SortDir = "asc" | "desc"

const LS_KEY = "krypto:watchlist"

export function useWatchlist() {
  const ids: Ref<Id[]> = ref<Id[]>([])
  const q = ref("")
  const sortBy = ref<SortKey>("asset")
  const sortDir = ref<SortDir>("asc")

  if (import.meta.client) {
    const raw = localStorage.getItem(LS_KEY)
    if (raw) {
      try {
        const parsed = JSON.parse(raw)
        if (Array.isArray(parsed)) ids.value = parsed.filter((x) => typeof x === "string")
      } catch {
      }
    }
  }

  function save() {
    if (import.meta.client) {
      localStorage.setItem(LS_KEY, JSON.stringify(ids.value))
    }
  }

  function toggle(id: Id) {
    const i = ids.value.indexOf(id)
    if (i === -1) ids.value.unshift(id)
    else ids.value.splice(i, 1)
    save()
  }

  function add(id: Id) {
    if (!ids.value.includes(id)) {
      ids.value.unshift(id)
      save()
    }
  }

  function remove(id: Id) {
    const next = ids.value.filter((x) => x !== id)
    if (next.length !== ids.value.length) {
      ids.value = next
      save()
    }
  }

  function reorder(from: number, to: number) {
    const len = ids.value.length
    if (len === 0 || from < 0 || from >= len) return

    const dest = Math.max(0, Math.min(to, len - 1))

    const [item] = ids.value.splice(from, 1) as [Id?]
    if (item === undefined) return

    ids.value.splice(dest, 0, item)
    save()
  }

  function setSort(key: SortKey) {
    if (sortBy.value === key) {
      sortDir.value = sortDir.value === "asc" ? "desc" : "asc"
    } else {
      sortBy.value = key
      sortDir.value = "desc"
    }
  }

  return {
    ids,
    q,
    sortBy,
    sortDir,
    toggle,
    add,
    remove,
    reorder,
    setSort,
  }
}
