import { useMemo, useState } from 'react'

import { getPriceChange } from '../utils/player'
import type { Player } from '../types/player'

type SortKey = 'name' | 'current_price' | 'average_price' | 'price_change'
type SortDirection = 'asc' | 'desc'

export function useMarketFilters(players: Player[]) {
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')
  const [sortKey, setSortKey] = useState<SortKey>('current_price')
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc')

  function toggleSort(key: SortKey) {
    if (key === sortKey) {
      setSortDirection((current) => current === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortDirection(key === 'name' ? 'asc' : 'desc')
    }
  }

  const filteredPlayers = useMemo(() => {
    const filtered = players.filter((player) => {
      const matchesSearch = player.name
        .toLowerCase()
        .includes(search.trim().toLowerCase())

      const matchesCategory =
        category === 'all' || player.category === category

      return matchesSearch && matchesCategory
    })


    return filtered.sort((a, b) => {
      if (sortKey === 'name') {
        const comparison = a.name.localeCompare(b.name)
        return sortDirection === 'asc' ? comparison : -comparison
      }

      const aValue =
        sortKey === 'price_change'
          ? getPriceChange(a)
          : a[sortKey]

      const bValue =
        sortKey === 'price_change'
          ? getPriceChange(b)
          : b[sortKey]

      if (aValue == null && bValue == null) return 0
      if (aValue == null) return 1
      if (bValue == null) return -1

      return sortDirection === 'asc'
        ? aValue - bValue
        : bValue - aValue
    })
    }, [players, search, category, sortKey, sortDirection])


  return {
    search,
    setSearch,
    category,
    setCategory,
    filteredPlayers,
    sortKey,
    sortDirection,
    toggleSort,
  }
}