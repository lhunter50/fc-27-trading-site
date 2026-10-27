import { useMemo, useState } from 'react'
import type { Player } from '../types/player'

export function useMarketFilters(players: Player[]) {
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')

  const filteredPlayers = useMemo(() => {
    return players.filter((player) => {
      const matchesSearch = player.name
        .toLowerCase()
        .includes(search.trim().toLowerCase())

      const matchesCategory =
        category === 'all' || player.category === category

      return matchesSearch && matchesCategory
    })
  }, [players, search, category])

  return {
    search,
    setSearch,
    category,
    setCategory,
    filteredPlayers,
  }
}