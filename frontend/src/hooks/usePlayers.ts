import { useEffect, useState } from 'react'
import { fetchPlayers } from '../services/api'
import type { Player } from '../types/player'

export function usePlayers() {
  const [players, setPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function loadPlayers() {
      try {
        const data = await fetchPlayers()

        if (!cancelled) {
          setPlayers(data.players)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Unknown error')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadPlayers()

    return () => {
      cancelled = true
    }
  }, [])

  return { players, loading, error }
}