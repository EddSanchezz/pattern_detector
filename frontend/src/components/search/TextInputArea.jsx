import { Textarea } from '../ui/Textarea';

export function TextInputArea({ value, onChange, placeholder = 'Ingresa o pega texto para detectar todos los patrones automáticamente...', disabled = false }) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-text-secondary">Texto de entrada</label>
      <Textarea
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={6}
        disabled={disabled}
      />
    </div>
  );
}