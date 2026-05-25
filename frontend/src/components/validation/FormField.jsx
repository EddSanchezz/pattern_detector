import { Input } from '../ui/Input';
import { ValidationBadge } from './ValidationBadge';

export function FormField({ label, value, onChange, pattern, status, error, placeholder }) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-text-primary">{label}</label>
      <div className="relative">
        <Input
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className={status === 'invalid' ? 'border-error focus:border-error focus:ring-error' : ''}
        />
        <div className="absolute right-3 top-1/2 -translate-y-1/2">
          <ValidationBadge status={status} />
        </div>
      </div>
      {status === 'invalid' && error && (
        <p className="text-sm text-error">{error}</p>
      )}
    </div>
  );
}