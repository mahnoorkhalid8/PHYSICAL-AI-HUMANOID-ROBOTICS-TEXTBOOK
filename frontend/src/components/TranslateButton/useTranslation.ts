import { useState } from 'react';
import { TranslationRequest, TranslationResponse } from './types';

interface UseTranslationResult {
  translateContent: (request: TranslationRequest, token: string) => Promise<void>;
  loading: boolean;
  error: string | null;
  result: TranslationResponse | null;
}

export const useTranslation = (): UseTranslationResult => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<TranslationResponse | null>(null);

  const translateContent = async (request: TranslationRequest, token: string) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // For Docusaurus, use relative URLs to work with proxy configuration
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text: request.text,
          preserve_technical_terms: request.preserve_technical_terms ?? true,
          source_language: request.source_language ?? 'en',
          target_language: request.target_language ?? 'ur'
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Translation request failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error('Translation error:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return {
    translateContent,
    loading,
    error,
    result
  };
};