import { PlayerTable } from './components/PlayerTable'
import { usePlayers } from './hooks/usePlayers'
import './App.css'

function App() {
  const { players, loading, error } = usePlayers()

  if (loading) return <p>Loading market data...</p>
  if (error) return <p>Error: {error}</p>

  return (
    <main>
      <h1>FC 27 Trading Scanner</h1>
      <p>Tracking {players.length} affordable players</p>

      <PlayerTable players={players} />
    </main>
  )
}

export default App