// Types for the translation feature

export interface TranslationRequest {
  content: string;
  preserve_technical_terms?: boolean;
  language_from?: string;
  language_to?: string;
}

export interface TranslationMetadata {
  processing_time: number;
  token_count: number;
  confidence_score: number;
}

export interface TranslationResponse {
  original_content: string;
  translated_content: string;
  language_from: string;
  language_to: string;
  translation_metadata: TranslationMetadata;
}

export interface TranslationSession {
  session_id: string;
  original_content: string;
  translated_content?: string;
  is_translating: boolean;
  translation_error?: string;
  view_mode: 'original' | 'translated' | 'side-by-side';
  timestamp: Date;
}