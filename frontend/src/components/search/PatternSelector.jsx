import { Checkbox } from '../ui/Checkbox';

const PATTERN_LABELS = {
  email: 'Correo electrónico',
  phone: 'Teléfono',
  date: 'Fecha',
  url: 'URL',
  plate: 'Placa de vehículo',
  document_id: 'Documento ID'
};

export function PatternSelector({ selectedPatterns, onTogglePattern, disabled = false }) {
  const patterns = Object.keys(PATTERN_LABELS);

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-text-secondary">Selecciona patrones</label>
      <div className="flex flex-wrap gap-4">
        {patterns.map((pattern) => (
          <Checkbox
            key={pattern}
            checked={selectedPatterns.includes(pattern)}
            onChange={() => onTogglePattern(pattern)}
            label={PATTERN_LABELS[pattern]}
            disabled={disabled}
          />
        ))}
      </div>
    </div>
  );
}