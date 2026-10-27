import type { PlayerResponse } from "../types/player"
import type { OpportunityResponse } from "../types/opportunity"

export async function fetchPlayers(): Promise<PlayerResponse> {
    const response = await fetch("/api/players")

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
    }

    return response.json()
}

export async function fetchOpportunities(): Promise<OpportunityResponse> {
    const response = await fetch("/api/opportunities")

    if (!response.ok) {
        throw new Error(`Failed to fetch opportunities: ${response.status}`)
    }

    return response.json()
}