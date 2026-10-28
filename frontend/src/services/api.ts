import type { PlayerResponse } from "../types/player"
import type { OpportunityResponse } from "../types/opportunity"
import type { ScannerSummary } from "../types/scanner"

export type MarketSource = "original" | "futgg"

export async function fetchPlayers(
    source: MarketSource = "original"
): Promise<PlayerResponse> {
    const endpoint = source === "futgg"
        ? "/api/futgg/players"
        : "/api/players"

    const response = await fetch(endpoint)

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

export async function fetchScannerSummary(): Promise<ScannerSummary> {
    const response = await fetch("/api/scanner/summary")

    if (!response.ok) {
        throw new Error(`Failed to fetch scanner summary: ${response.status}`)
    }

    return response.json()
}