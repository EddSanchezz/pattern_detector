export function Card({ children, className = '' }) {
  return (
    <div className={`bg-bg-secondary rounded-xl border border-text-secondary/10 p-6 ${className}`}>
      {children}
    </div>
  );
}