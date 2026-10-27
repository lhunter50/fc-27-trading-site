import type { ScannerSummary as ScannerSummaryType } from '../../types/scanner'

interface ScannerSummaryProps {
  summary: ScannerSummaryType
}

export function ScannerSummary({ summary }: ScannerSummaryProps) {
  const stats = [
    { label: 'Players Analyzed', value: summary.players_analyzed },
    { label: 'Below Average', value: summary.below_average },
    { label: 'Rejected After Tax', value: summary.rejected_after_tax },
    { label: 'Profitable Opportunities', value: summary.profitable_opportunities },
  ]

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="rounded-xl border border-slate-800 bg-slate-900 p-6"
        >
          <p className="text-sm text-slate-400">{stat.label}</p>
          <p className="mt-2 text-3xl font-bold text-white">
            {stat.value.toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  )
}