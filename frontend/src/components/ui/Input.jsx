export function Input({ value, onChange, placeholder, disabled, className = '' }) {
  return (
    <input
      type="text"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      disabled={disabled}
      className={`w-full px-4 py-3 bg-bg-secondary border border-text-secondary/20 rounded-lg text-text-primary placeholder:text-text-secondary/50 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
    />
  );
}