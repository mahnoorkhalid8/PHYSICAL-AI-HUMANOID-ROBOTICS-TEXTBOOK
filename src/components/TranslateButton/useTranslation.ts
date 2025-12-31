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
      console.log('Starting translation request with content length:', request.content.length);
      console.log('Request payload:', {
        content: request.content.substring(0, 100) + '...', // First 100 chars for debugging
        preserve_technical_terms: request.preserve_technical_terms ?? true,
        language_from: request.language_from ?? 'en',
        language_to: request.language_to ?? 'ur'
      });

      // For Docusaurus, use relative URLs to work with proxy configuration
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          content: request.content,
          preserve_technical_terms: request.preserve_technical_terms ?? true,
          language_from: request.language_from ?? 'en',
          language_to: request.language_to ?? 'ur'
        })
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Translation API error response:', errorData);
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Translation response received:', data);
      setResult(data);
    } catch (err) {
      console.error('Translation error:', err);
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      console.error('Full error details:', err);
      setError(errorMessage);
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