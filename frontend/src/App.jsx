import { useState } from 'react';
import { Header } from './components/layout/Header';
import { TabNavigation } from './components/layout/TabNavigation';
import { PatternSearch } from './components/search/PatternSearch';
import { FormValidation } from './components/validation/FormValidation';

function App() {
  const [activeTab, setActiveTab] = useState('search');

  return (
    <div className="min-h-screen flex flex-col bg-bg-primary">
      <Header />
      <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="flex-1">
        {activeTab === 'search' && <PatternSearch />}
        {activeTab === 'validate' && <FormValidation />}
      </main>
      <footer className="bg-bg-secondary border-t border-text-secondary/10 py-4">
        <p className="text-center text-sm text-text-secondary">
          PatternGuard - Sistema de Búsqueda y Validación de Patrones
        </p>
      </footer>
    </div>
  );
}

export default App;