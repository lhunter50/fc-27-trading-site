import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { DashboardLayout } from './components/layout/DashboardLayout'
import { MarketPage } from './pages/MarketPage'
import { InvestmentsPage } from './pages/InvestmentPage'

function App() {
  return (
    <BrowserRouter>
      <DashboardLayout>
        <Routes>
          <Route path="/" element={<MarketPage />} />
          <Route path="/investments" element={<InvestmentsPage />} />
        </Routes>
      </DashboardLayout>
    </BrowserRouter>
  )
}

export default App