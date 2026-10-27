import {useEffect, useState} from "react";
import {fetchScannerSummary} from "../services/api";
import type {ScannerSummary} from "../types/scanner";

export function useScannerSummary() {
    const [summary, setSummary] = useState<ScannerSummary | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let cancelled = false;

        async function loadSummary() {
            try {
                const data = await fetchScannerSummary();
                if (!cancelled) {
                    setSummary(data);
                    setLoading(false);
                }
            } catch (err) {
                if (!cancelled) {
                    setError((err as Error).message);
                    setLoading(false);
                }
            }
        }

        loadSummary();

        return () => {
            cancelled = true;
        };
    }, []);

    return { summary, loading, error };
}