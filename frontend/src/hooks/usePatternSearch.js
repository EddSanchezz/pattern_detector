import { useState, useCallback } from 'react';
import { searchPatterns } from '../services/api';

const ALL_PATTERNS = ['email', 'phone', 'date', 'url', 'plate', 'document_id'];

export function usePatternSearch() {
  const [text, setText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = useCallback(async () => {
    if (!text.trim()) {
      setError('Ingresa texto para buscar patrones');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await searchPatterns(text, ALL_PATTERNS);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [text]);

  return {
    text,
    setText,
    results,
    loading,
    error,
    search
  };
}