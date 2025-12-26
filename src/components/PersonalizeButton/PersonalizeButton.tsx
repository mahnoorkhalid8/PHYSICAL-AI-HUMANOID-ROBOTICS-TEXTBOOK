import React, { useState } from 'react';
import { useAuth } from './useAuth';
import { usePersonalization } from './usePersonalization';
import PersonalizeModal from '../PersonalizeModal/PersonalizeModal';
import './styles.css';

interface PersonalizeButtonProps {
  chapterContent: string;
  chapterTitle?: string;
  className?: string;
}

const PersonalizeButton: React.FC<PersonalizeButtonProps> = ({
  chapterContent,
  chapterTitle = 'Current Chapter',
  className = ''
}) => {
  const { user, isLoading: authLoading } = useAuth();
  const {
    personalizeContent,
    loading,
    error,
    result
  } = usePersonalization();

  const [isModalOpen, setIsModalOpen] = useState(false);

  const handlePersonalize = async () => {
    if (!user) {
      alert('Please log in to access personalization features');
      return;
    }

    try {
      await personalizeContent({
        chapter_content: chapterContent,
        chapter_title: chapterTitle,
        user_id: user.id,
        user_background: {
          software: user.software_background || 'Beginner',
          hardware: user.hardware_background || 'Beginner'
        }
      });

      setIsModalOpen(true);
    } catch (err) {
      console.error('Personalization error:', err);
      alert(`Error during personalization: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className={`personalize-container ${className}`}>
      <button
        onClick={handlePersonalize}
        disabled={authLoading || loading}
        className={`personalize-button ${authLoading || loading ? 'button-loading' : ''}`}
        title="Personalize this content based on your background"
      >
        {loading ? (
          <span className="button-spinner">Personalizing...</span>
        ) : (
          <span>Personalize This Chapter</span>
        )}
      </button>

      <PersonalizeModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        content={result?.personalized_content || ''}
        reasoning={result?.personalization_reasoning || ''}
        error={error}
        processingTime={result?.processing_time_ms}
      />
    </div>
  );
};

export default PersonalizeButton;