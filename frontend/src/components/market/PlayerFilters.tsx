interface PlayerFiltersProps {
    search: string
    category: string
    onSearchChange: (search: string) => void
    onCategoryChange: (category: string) => void
}

export function PlayerFilters({
    search,
    category,
    onSearchChange,
    onCategoryChange,
}: PlayerFiltersProps) {
    return (    
    <div className="flex flex-wrap items-center gap-4">
        <input
            type="text"
            placeholder="Search players..."
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            className="min-w-56 flex-1 rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
        />

        <select
            value={category}
            onChange={(e) => onCategoryChange(e.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none focus:border-indigo-500"
        >
            <option value="all">All Players</option>
            <option value="budget">Budget (1K–10K)</option>
            <option value="mid_range">Mid-range (10K–100K)</option>
        </select>
    </div>
    )
}