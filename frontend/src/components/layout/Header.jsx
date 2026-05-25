import { Search, FileCheck } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-bg-secondary border-b border-text-secondary/10">
      <div className="max-w-5xl mx-auto px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-accent/20 flex items-center justify-center">
            <svg className="w-6 h-6 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-semibold text-text-primary">PatternGuard</h1>
            <p className="text-sm text-text-secondary">Detección y validación de patrones</p>
          </div>
        </div>
      </div>
    </header>
  );
}