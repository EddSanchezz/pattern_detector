import { Search, FileCheck } from 'lucide-react';

export function TabNavigation({ activeTab, onTabChange }) {
  const tabs = [
    { id: 'search', label: 'Búsqueda de Patrones', icon: Search },
    { id: 'validate', label: 'Validación de Formularios', icon: FileCheck }
  ];

  return (
    <nav className="bg-bg-secondary border-b border-text-secondary/10">
      <div className="max-w-5xl mx-auto px-6">
        <div className="flex gap-1">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-all ${
                  isActive
                    ? 'border-accent text-accent'
                    : 'border-transparent text-text-secondary hover:text-text-primary hover:border-text-secondary/30'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
}