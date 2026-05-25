export function Textarea({ value, onChange, placeholder, rows = 6, disabled = false, className = '' }) {
  return (
    <textarea
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      rows={rows}
      disabled={disabled}
      className={`w-full px-4 py-3 bg-bg-secondary border border-text-secondary/20 rounded-lg text-text-primary placeholder:text-text-secondary/50 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all resize-none ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
    />
  );
}