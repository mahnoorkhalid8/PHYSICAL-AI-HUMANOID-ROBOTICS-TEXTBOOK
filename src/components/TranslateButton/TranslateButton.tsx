import React, { useState } from 'react';
import { useAuth } from '../PersonalizeButton/useAuth'; // Reuse the existing auth hook
import { useTranslation } from './useTranslation';
import TranslateModal from './TranslateModal';
import './styles.css';

interface TranslateButtonProps {
  chapterContent: string;
  chapterTitle?: string;
  className?: string;
}

const TranslateButton: React.FC<TranslateButtonProps> = ({
  chapterContent,
  chapterTitle = 'Current Chapter',
  className = ''
}) => {
  const { user, isLoading: authLoading, getToken } = useAuth();
  const {
    translateContent,
    loading,
    error,
    result
  } = useTranslation();

  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleTranslate = async () => {
    console.log('Translate button clicked');
    console.log('Chapter content length:', chapterContent.length);
    console.log('Chapter content preview:', chapterContent.substring(0, 100) + '...');

    if (!user) {
      alert('Please log in to access translation features');
      return;
    }

    try {
      // Get the authentication token
      const token = await getToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      console.log('Token retrieved, proceeding with translation');

      await translateContent({
        content: chapterContent,
        language_to: 'ur', // Urdu translation
        preserve_technical_terms: true
      }, token);

      setIsModalOpen(true);
    } catch (err) {
      console.error('Translation error:', err);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className={`translate-container ${className}`}>
      <button
        onClick={handleTranslate}
        disabled={authLoading || loading}
        className={`translate-button ${authLoading || loading ? 'button-loading' : ''}`}
        title="Translate this content to Urdu"
      >
        {loading ? (
          <span className="button-spinner">Translating...</span>
        ) : (
          <span>Translate to Urdu</span>
        )}
      </button>

      <TranslateModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        originalContent={result?.original_content || ''}
        translatedContent={result?.translated_content || ''}
        error={error}
        processingTime={result?.translation_metadata?.processing_time}
      />
    </div>
  );
};

export default TranslateButton;