import type { Player } from '../../types/player'

interface MarketSummaryProps {
  players: Player[]
}

export function MarketSummary({ players }: MarketSummaryProps) {
  const budget = players.filter(
    (player) => player.category === 'budget'
  ).length

  const midRange = players.filter(
    (player) => player.category === 'mid_range'
  ).length

  const stats = [
    { label: 'Tracked Players', value: players.length },
    { label: 'Budget Cards', value: budget },
    { label: 'Mid-range Cards', value: midRange },
  ]

  return (
    <div className="grid gap-4 sm:grid-cols-3">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="rounded-xl border border-slate-800 bg-slate-900 p-6"
        >
          <p className="text-sm text-slate-400">
            {stat.label}
          </p>

          <p className="mt-2 text-3xl font-bold text-white">
            {stat.value.toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  )
}