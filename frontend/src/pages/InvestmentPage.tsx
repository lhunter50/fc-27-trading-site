import { OpportunityTable } from '../components/investments/OpportunityTable'
import { useOpportunities } from '../hooks/useOpportunities'

export function InvestmentsPage() {
  const { opportunities, loading, error } = useOpportunities()

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">
          Investment Opportunities
        </h2>

        <p className="mt-2 text-slate-400">
          Players currently priced below their historical averages.
        </p>
      </div>

      {loading && <p>Scanning market opportunities...</p>}

      {error && <p className="text-red-400">Error: {error}</p>}

      {!loading && !error && (
        <>
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <p className="text-sm text-slate-400">
              Potential Opportunities
            </p>

            <p className="mt-2 text-3xl font-bold text-white">
              {opportunities.length}
            </p>
          </div>

          <OpportunityTable opportunities={opportunities} />

          <p className="text-xs text-slate-500">
            Estimated profits assume a sale at the historical average
            after a 5% market tax. These are hypothetical returns,
            not guaranteed trading profits.
          </p>
        </>
      )}
    </div>
  )
}