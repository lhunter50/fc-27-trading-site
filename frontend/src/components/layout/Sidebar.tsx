const navigation = [
  { label: 'Market', icon: '📊' },
  { label: 'Investments', icon: '📈' },
  { label: 'Portfolio', icon: '💼' },
]

export function Sidebar() {
  return (
    <aside className="w-60 shrink-0 border-r border-slate-800 bg-slate-950 p-6">
      <div className="mb-10">
        <h1 className="text-xl font-bold text-white">
          FC 27 Trader
        </h1>
        <p className="mt-1 text-xs text-slate-400">
          Ultimate Team Analytics
        </p>
      </div>

      <nav className="space-y-2">
        {navigation.map((item) => (
          <div
            key={item.label}
            className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm ${
              item.label === 'Market'
                ? 'bg-indigo-600/20 font-medium text-indigo-400'
                : 'text-slate-400'
            }`}
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </div>
        ))}
      </nav>
    </aside>
  )
}