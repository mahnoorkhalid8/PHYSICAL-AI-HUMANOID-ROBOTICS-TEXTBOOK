import { useState } from 'react';
import axios from 'axios';
import { useAuth } from './useAuth';
import { PersonalizeRequest, PersonalizeResponse } from './types';

interface PersonalizationState {
  loading: boolean;
  error: string | null;
  result: PersonalizeResponse | null;
}

export const usePersonalization = () => {
  const [state, setState] = useState<PersonalizationState>({
    loading: false,
    error: null,
    result: null
  });

  const personalizeContent = async (request: PersonalizeRequest, token: string): Promise<void> => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      if (!token) {
        throw new Error('No authentication token available');
      }

      // For Docusaurus, use relative URLs to work with proxy configuration
      // This allows the request to go through the Docusaurus proxy to the backend
      const apiUrl = '/api/personalize';

      const response = await axios.post<PersonalizeResponse>(
        apiUrl,
        request,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      setState({
        loading: false,
        error: null,
        result: response.data
      });
    } catch (error: any) {
      let errorMessage = 'An error occurred during personalization';

      if (error.response) {
        // Server responded with error status
        if (error.response.status === 401) {
          errorMessage = 'Authentication required. Please log in.';
        } else if (error.response.status === 403) {
          errorMessage = 'Access denied. Please check your permissions.';
        } else if (error.response.status === 429) {
          errorMessage = 'Too many requests. Please try again later.';
        } else {
          errorMessage = error.response.data?.error || errorMessage;
        }
      } else if (error.request) {
        // Request was made but no response received
        errorMessage = 'Network error. Please check your connection.';
      } else {
        // Something else happened
        errorMessage = error.message || errorMessage;
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