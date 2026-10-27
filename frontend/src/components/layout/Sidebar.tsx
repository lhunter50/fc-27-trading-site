import { NavLink } from 'react-router-dom'

const navigation = [
  { label: 'Market', path: '/', icon: '📊' },
  { label: 'Investments', path: '/investments', icon: '📈' },
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
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-4 py-3 text-sm transition-colors ${
                isActive
                  ? 'bg-indigo-600/20 font-medium text-indigo-400'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}