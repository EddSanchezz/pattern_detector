export function Checkbox({ checked, onChange, label, disabled = false }) {
  return (
    <label className={`flex items-center gap-2 cursor-pointer select-none ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}>
      <div
        onClick={() => !disabled && onChange(!checked)}
        className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-all ${
          checked 
            ? 'bg-accent border-accent' 
            : 'border-text-secondary/40 hover:border-accent'
        }`}
      >
        {checked && (
          <svg className="w-3 h-3 text-bg-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        )}
      </div>
      <span className="text-text-primary text-sm">{label}</span>
    </label>
  );
}