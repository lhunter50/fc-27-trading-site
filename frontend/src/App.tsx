import { DashboardLayout } from './components/layout/DashboardLayout'
import { MarketSummary } from './components/market/MarketSummary'
import { PlayerTable } from './components/market/PlayerTable'
import { usePlayers } from './hooks/usePlayers'

function App() {
  const { players, loading, error } = usePlayers()

  return (
    <DashboardLayout>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white">
          Market Overview
        </h2>
        <p className="mt-2 text-slate-400">
          Monitor player prices and discover trading opportunities.
        </p>
      </div>

      {loading && <p>Loading market data...</p>}

      {error && (
        <p className="text-red-400">
          Error: {error}
        </p>
      )}

      {!loading && !error && (
        <div className="space-y-8">
          <MarketSummary players={players} />
          <PlayerTable players={players} />
        </div>
      )}
    </DashboardLayout>
  )
}

export default App