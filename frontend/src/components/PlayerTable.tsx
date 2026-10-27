import type { Player } from '../types/player'

interface PlayerTableProps {
  players: Player[]
}

export function PlayerTable({ players }: PlayerTableProps) {
  return (
    <table>
      <thead>
        <tr>
          <th>Player</th>
          <th>Category</th>
          <th>Current Price</th>
          <th>Average Price</th>
          <th>Price Change</th>
        </tr>
      </thead>

      <tbody>
        {players.map((player) => (
          <tr key={player.player_id}>
            <td>{player.name}</td>
            <td>{player.category}</td>
            <td>{player.current_price.toLocaleString()}</td>
            <td>{player.average_price.toLocaleString()}</td>
            <td>
              {player.price_change === null
                ? 'N/A'
                : `${player.price_change}%`}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}