export interface Opportunity {
    player_id: number
    name: string
    category: string
    current_price: number
    average_price: number
    potential_profit: number
    roi: number
    observations: number
}
export interface OpportunityResponse {
    count: number
    opportunities: Opportunity[]
}