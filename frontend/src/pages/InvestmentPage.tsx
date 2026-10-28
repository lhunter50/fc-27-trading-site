import { useState } from 'react'

import type { MarketSource } from '../services/api'

import { OpportunityTable } from '../components/investments/OpportunityTable'
import { useOpportunities } from '../hooks/useOpportunities'
import { ScannerSummary } from '../components/investments/ScannerSummary'
import { useScannerSummary } from '../hooks/useScannerSummary'

export function InvestmentsPage() {
  const [source, setSource ] = useState<MarketSource>('futgg')
  const { opportunities, loading, error } = useOpportunities(source)
  const { summary, loading: scannerLoading, error: scannerError } = useScannerSummary()
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
      <div className="flex gap-2">
        {(['futgg', 'original'] as const).map((option) => (
          <button
            key={option}
            type="button"
            onClick={() => setSource(option)}
            className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
              source === option
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            {option === 'futgg' ? 'FUT.GG' : 'Original Market'}
          </button>
        ))}
      </div>

      {scannerLoading && <p>Scanning market opportunities...</p>}

      {scannerError && <p className="text-red-400">Error: {scannerError}</p>}

      {!scannerLoading && !scannerError && summary && (
        <ScannerSummary summary={summary} />
      )}

      {loading && <p>Scanning market opportunities...</p>}

      {error && <p className="text-red-400">Error: {error}</p>}

      {!loading && !error && (
        <>

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