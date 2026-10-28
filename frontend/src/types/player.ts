export interface Player {
    player_id: number
    name: string
    current_price: number
    average_price: number
    price_change?: number | null
    category: string
    observations: number
}

export interface PlayerResponse {
    count: number
    players: Player[]
}