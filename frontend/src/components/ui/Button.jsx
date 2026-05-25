export function Button({ children, onClick, disabled, variant = 'primary', className = '', type = 'button' }) {
  const baseStyles = 'px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-accent hover:bg-accent-hover text-bg-primary',
    secondary: 'bg-bg-elevated hover:bg-bg-secondary text-text-primary border border-text-secondary/20',
    success: 'bg-success hover:brightness-110 text-white'
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyles} ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
}