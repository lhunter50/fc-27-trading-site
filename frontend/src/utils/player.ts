import type { Player } from '../types/player'

export function getPriceChange(player: Player): number | null {
  if (player.price_change != null) {
    return player.price_change
  }

  if (player.average_price <= 0) {
    return null
  }

  return (
    ((player.current_price - player.average_price) /
      player.average_price) * 100
  )
}