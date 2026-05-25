import { useMemo } from 'react';
import { Badge } from '../ui/Badge';
import { Card } from '../ui/Card';

const PATTERN_NAMES = {
  email: 'Email',
  phone: 'Teléfono',
  date: 'Fecha',
  url: 'URL',
  plate: 'Placa',
  document_id: 'Documento ID'
};

export function SearchResults({ results }) {
  const allMatches = useMemo(() => {
    if (!results?.matches) return [];
    const matches = [];
    for (const [pattern, data] of Object.entries(results.matches)) {
      // data is directly an array of matches, not an object with .matches property
      if (Array.isArray(data)) {
        for (const match of data) {
          matches.push({ pattern, ...match });
        }
      }
    }
    return matches.sort((a, b) => a.start - b.start);
  }, [results]);

  if (!results) {
    return (
      <Card className="text-center py-12">
        <p className="text-text-secondary">Ingresa texto y selecciona patrones para buscar</p>
      </Card>
    );
  }

  if (allMatches.length === 0) {
    return (
      <Card className="text-center py-12">
        <p className="text-text-secondary">No se encontraron coincidencias</p>
      </Card>
    );
  }

  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium text-text-primary">
            Resultados ({results.total_matches} matches)
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-text-secondary/10">
                <th className="text-left text-xs font-medium text-text-secondary uppercase tracking-wide py-2 pr-4">Tipo</th>
                <th className="text-left text-xs font-medium text-text-secondary uppercase tracking-wide py-2 pr-4">Valor</th>
                <th className="text-left text-xs font-medium text-text-secondary uppercase tracking-wide py-2">Posición</th>
              </tr>
            </thead>
            <tbody>
              {allMatches.map((match, index) => (
                <tr key={index} className="border-b border-text-secondary/5 hover:bg-bg-elevated/50">
                  <td className="py-3 pr-4">
                    <Badge variant="default">{PATTERN_NAMES[match.pattern] || match.pattern}</Badge>
                  </td>
                  <td className="py-3 pr-4">
                    <code className="text-sm bg-bg-elevated px-2 py-1 rounded text-accent">{match.value}</code>
                  </td>
                  <td className="py-3 text-sm text-text-secondary">
                    {match.start + 1} - {match.end}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Card>
  );
}