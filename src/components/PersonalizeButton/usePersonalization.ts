import { useState } from 'react';
import { useAuth } from './useAuth';

interface PersonalizationState {
  loading: boolean;
  error: string | null;
  result: PersonalizeResponse | null;
}

export const usePersonalization = () => {
  const { getToken } = useAuth(); // Get the getToken function from auth context
  const [state, setState] = useState<PersonalizationState>({
    loading: false,
    error: null,
    result: null
  });

  const personalizeContent = async (request: PersonalizeRequest): Promise<void> => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      console.log('Personalization request:', request);

      // Get the JWT token from auth context
      const token = await getToken();

      if (!token) {
        throw new Error('No authentication token available. Please log in again.');
      }

      // Call the actual backend API for personalization
      const response = await fetch('/api/personalize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          chapter_content: request.chapter_content,
          chapter_title: request.chapter_title,
          user_id: request.user_id,
          user_background: request.user_background
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || `HTTP error! Status: ${response.status}`;

        // If it's a token validation error, clear the invalid token
        if (response.status === 401 || errorMessage.toLowerCase().includes('token') || errorMessage.toLowerCase().includes('validation')) {
          // Try to clear the invalid token from auth context
          console.error('Token validation failed, clearing invalid token');
        }

        throw new Error(errorMessage);
      }

      const result: PersonalizeResponse = await response.json();

      setState({
        loading: false,
        error: null,
        result: result
      });
    } catch (error: any) {
      let errorMessage = 'An error occurred during personalization';

      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        errorMessage = 'Network error. Please check your connection.';
      } else if (error.message && error.message.toLowerCase().includes('token validation failed')) {
        errorMessage = 'Authentication token is invalid. Please log out and log back in to refresh your session.';
      } else if (error.message) {
        errorMessage = error.message;
      } else {
        errorMessage = 'An unknown error occurred during personalization.';
      }

      setState({
        loading: false,
        error: errorMessage,
        result: null
      });

      throw new Error(errorMessage);
    }
  };

  const resetState = () => {
    setState({
      loading: false,
      error: null,
      result: null
    });
  };

  return {
    ...state,
    personalizeContent,
    resetState
  };
};

// Define types for personalization if not already defined
export interface PersonalizeRequest {
  chapter_content: string;
  chapter_title?: string;
  user_id: string;
  user_background: {
    software: string;
    hardware: string;
  };
}

export interface PersonalizeResponse {
  id: string;
  personalized_content: string;
  personalization_reasoning: string;
  generated_at: string;
  processing_time_ms: number;
}