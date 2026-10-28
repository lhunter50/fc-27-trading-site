import { useEffect, useState } from 'react'
import { fetchOpportunities } from '../services/api'
import type { MarketSource } from '../services/api'
import type { Opportunity } from '../types/opportunity'

export function useOpportunities(
  source: MarketSource = 'original'
) {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function loadOpportunities() {
      setLoading(true)
      setError(null)

      try {
        const data = await fetchOpportunities(source)

        if (!cancelled) {
          setOpportunities(data.opportunities)
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error ? err.message : 'Unknown error'
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadOpportunities()

    return () => {
      cancelled = true
    }
  }, [source])

  return { opportunities, loading, error }
}