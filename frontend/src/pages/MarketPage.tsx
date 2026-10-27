import { MarketSummary } from '../components/market/MarketSummary'
import { PlayerFilters } from '../components/market/PlayerFilters'
import { PlayerTable } from '../components/market/PlayerTable'
import { usePlayers } from '../hooks/usePlayers'
import { useMarketFilters } from '../hooks/useMarketFilters'

export function MarketPage() {
  const { players, loading, error } = usePlayers()

  const {
    search,
    setSearch,
    category,
    setCategory,
    filteredPlayers,
    sortKey,
    sortDirection,
    toggleSort,
  } = useMarketFilters(players)

  return (
    <>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white">
          Market Overview
        </h2>
        <p className="mt-2 text-slate-400">
          Monitor player prices and discover trading opportunities.
        </p>
      </div>

      {loading && <p>Loading market data...</p>}

      {error && <p className="text-red-400">Error: {error}</p>}

      {!loading && !error && (
        <div className="space-y-8">
          <MarketSummary players={players} />

          <section className="space-y-4">
            <PlayerFilters
              search={search}
              category={category}
              onSearchChange={setSearch}
              onCategoryChange={setCategory}
            />

            <p className="text-sm text-slate-400">
              Showing {filteredPlayers.length} of {players.length} players
            </p>

            <PlayerTable
              players={filteredPlayers}
              sortKey={sortKey}
              sortDirection={sortDirection}
              onSort={toggleSort}
            />
          </section>
        </div>
      )}
    </>
  )
}