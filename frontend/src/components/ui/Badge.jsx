export function Badge({ children, variant = 'default' }) {
  const variants = {
    default: 'bg-bg-elevated text-text-primary',
    success: 'bg-success/20 text-success',
    error: 'bg-error/20 text-error',
    warning: 'bg-warning/20 text-warning'
  };

  return (
    <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${variants[variant]}`}>
      {children}
    </span>
  );
}