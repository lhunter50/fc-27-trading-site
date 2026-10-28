import { useEffect, useState } from "react"
import { fetchScannerSummary } from "../services/api"
import type { MarketSource } from "../services/api"
import type {
    ScannerSummary,
    FutggScannerSummary
} from "../types/scanner"

export function useScannerSummary(
    source: MarketSource = "original"
) {
    const [summary, setSummary] = useState<
        ScannerSummary | FutggScannerSummary | null
    >(null)

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        let cancelled = false

        async function loadSummary() {
            setLoading(true)
            setError(null)
            setSummary(null)

            try {
                const data = await fetchScannerSummary(source)

                if (!cancelled) {
                    setSummary(data)
                }
            } catch (err) {
                if (!cancelled) {
                    setError(
                        err instanceof Error
                            ? err.message
                            : "Unknown error"
                    )
                }
            } finally {
                if (!cancelled) {
                    setLoading(false)
                }
            }
        }

        loadSummary()

        return () => {
            cancelled = true
        }
    }, [source])

    return { summary, loading, error }
}