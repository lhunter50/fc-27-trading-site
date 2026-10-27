import type { PlayerResponse } from "../types/player"

export async function fetchPlayers(): Promise<PlayerResponse> {
    const response = await fetch("/api/players")

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
    }

    return response.json()
}