import type { Player } from '../../types/player'
import { getPriceChange } from '../../utils/player'

type SortKey = 'name' | 'current_price' | 'average_price' | 'price_change'

interface PlayerTableProps {
  players: Player[]
  sortKey: SortKey
  sortDirection: 'asc' | 'desc'
  onSort: (key: SortKey) => void
}

export function PlayerTable({
  players,
  sortKey,
  sortDirection,
  onSort,
}: PlayerTableProps) {
  function sortHeader(label: string, key: SortKey) {
    return (
      <button
        type="button"
        onClick={() => onSort(key)}
        className="flex items-center gap-2 hover:text-white"
      >
        {label}
        <span className="text-indigo-400">
          {sortKey === key ? (sortDirection === 'asc' ? '↑' : '↓') : '↕'}
        </span>
      </button>
    )
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-slate-800 bg-slate-950/60 text-slate-400">
          <tr>
            <th className="px-5 py-4">{sortHeader('Player', 'name')}</th>
            <th className="px-5 py-4">Category</th>
            <th className="px-5 py-4">{sortHeader('Current Price', 'current_price')}</th>
            <th className="px-5 py-4">{sortHeader('Average Price', 'average_price')}</th>
            <th className="px-5 py-4">{sortHeader('Price Change', 'price_change')}</th>
          </tr>
        </thead>


        <tbody className="divide-y divide-slate-800">
          {players.map((player) => {
            const priceChange = getPriceChange(player)

            return (
              <tr key={player.player_id} className="hover:bg-slate-800/50">
                <td className="px-5 py-4 font-medium text-white">
                  {player.name}
                </td>

                <td className="px-5 py-4 capitalize text-slate-400">
                  {player.category.replace('_', ' ')}
                </td>

                <td className="px-5 py-4">
                  {player.current_price.toLocaleString()}
                </td>

                <td className="px-5 py-4">
                  {player.average_price.toLocaleString()}
                </td>

                <td className={`px-5 py-4 font-medium ${
                  priceChange === null
                    ? 'text-slate-500'
                    : priceChange > 0
                      ? 'text-emerald-400'
                      : priceChange < 0
                        ? 'text-red-400'
                        : 'text-slate-400'
                }`}>
                  {priceChange === null
                    ? 'N/A'
                    : `${priceChange > 0 ? '+' : ''}${priceChange.toFixed(2)}%`}
                </td>
              </tr>
            )
          })}
        </tbody>

      </table>

      {players.length === 0 && (
        <p className="p-8 text-center text-slate-400">
          No players match your filters.
        </p>
      )}
    </div>
  )
}