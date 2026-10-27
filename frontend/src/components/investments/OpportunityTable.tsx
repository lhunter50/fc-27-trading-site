import type { Opportunity } from '../../types/opportunity'

interface OpportunityTableProps {
  opportunities: Opportunity[]
}

export function OpportunityTable({ opportunities }: OpportunityTableProps) {
  return (
    <div className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-slate-800 bg-slate-950/60 text-slate-400">
          <tr>
            <th className="px-5 py-4">Player</th>
            <th className="px-5 py-4">Buy Price</th>
            <th className="px-5 py-4">Historical Average</th>
            <th className="px-5 py-4">Potential Profit</th>
            <th className="px-5 py-4">ROI</th>
            <th className="px-5 py-4">Observations</th>
          </tr>
        </thead>

        <tbody className="divide-y divide-slate-800">
          {opportunities.map((player) => (
            <tr
              key={player.player_id}
              className="hover:bg-slate-800/50"
            >
              <td className="px-5 py-4 font-medium text-white">
                {player.name}
              </td>

              <td className="px-5 py-4">
                {player.current_price.toLocaleString()}
              </td>

              <td className="px-5 py-4">
                {player.average_price.toLocaleString()}
              </td>

              <td className="px-5 py-4 text-emerald-400">
                +{player.potential_profit.toLocaleString()}
              </td>

              <td className="px-5 py-4 font-medium text-emerald-400">
                +{player.roi.toFixed(2)}%
              </td>

              <td className="px-5 py-4 text-slate-400">
                {player.observations}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {opportunities.length === 0 && (
        <p className="p-8 text-center text-slate-400">
          No profitable opportunities detected yet.
        </p>
      )}
    </div>
  )
}