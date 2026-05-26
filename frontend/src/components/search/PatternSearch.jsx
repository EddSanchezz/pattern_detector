import { Search } from 'lucide-react';
import { TextInputArea } from './TextInputArea';
import { SearchResults } from './SearchResults';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';
import { usePatternSearch } from '../../hooks/usePatternSearch';

const PATTERN_EXAMPLES = [
  { pattern: 'email', icon: '📧', example: 'usuario@ejemplo.com' },
  { pattern: 'phone', icon: '📱', example: '3217539293, +57 3...' },
  { pattern: 'date', icon: '📅', example: 'DD/MM/YYYY (25/12/2024)' },
  { pattern: 'url', icon: '🔗', example: 'https://...' },
  { pattern: 'plate', icon: '🚗', example: 'ABC-123, HLQ-75E' },
  { pattern: 'document_id', icon: '🪪', example: 'CC1006538374' },
  { pattern: 'password', icon: '🔐', example: 'Pass123@' }
];

export function PatternSearch() {
  const { text, setText, results, loading, error, search } = usePatternSearch();

  return (
    <div className="max-w-5xl mx-auto px-6 py-8 space-y-6">
      <Card>
        <div className="space-y-6">
          <TextInputArea
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          
          <div className="bg-bg-elevated rounded-lg p-4">
            <p className="text-sm font-medium text-accent mb-3">Patrones detectados automáticamente:</p>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {PATTERN_EXAMPLES.map(({ pattern, icon, example }) => (
                <div key={pattern} className="flex items-center gap-2 text-xs text-text-secondary">
                  <span>{icon}</span>
                  <span className="capitalize">{pattern.replace('_', ' ')}:</span>
                  <span className="text-text-primary/70 font-mono">{example}</span>
                </div>
              ))}
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <Button onClick={search} disabled={loading}>
              <Search className="w-4 h-4" />
              {loading ? 'Buscando...' : 'Buscar Patrones'}
            </Button>
            {error && (
              <p className="text-sm text-error">{error}</p>
            )}
          </div>
        </div>
      </Card>
      <SearchResults results={results} />
    </div>
  );
}