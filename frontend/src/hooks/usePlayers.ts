import { useEffect, useState } from "react"
import { fetchPlayers } from "../services/api"
import type { MarketSource } from "../services/api"
import type { Player } from "../types/player"

export function usePlayers(source: MarketSource = "original") {
    const [players, setPlayers] = useState<Player[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        let cancelled = false

        async function loadPlayers() {
            setLoading(true)
            setError(null)

            try {
                const data = await fetchPlayers(source)

                if (!cancelled) {
                    setPlayers(data.players)
                }
            } catch (err) {
                if (!cancelled) {
                    setError(
                        err instanceof Error
                            ? err.message
                            : "Unknown error"
                    )
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
    }, [source])

    return { players, loading, error }
}