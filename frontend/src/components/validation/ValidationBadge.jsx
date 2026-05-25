import { CheckCircle, XCircle, Loader } from 'lucide-react';

export function ValidationBadge({ status }) {
  if (status === 'loading') {
    return (
      <div className="flex items-center gap-1 text-text-secondary">
        <Loader className="w-4 h-4 animate-spin" />
      </div>
    );
  }

  if (status === 'valid') {
    return (
      <div className="flex items-center gap-1 text-success">
        <CheckCircle className="w-4 h-4" />
      </div>
    );
  }

  if (status === 'invalid') {
    return (
      <div className="flex items-center gap-1 text-error">
        <XCircle className="w-4 h-4" />
      </div>
    );
  }

  return null;
}