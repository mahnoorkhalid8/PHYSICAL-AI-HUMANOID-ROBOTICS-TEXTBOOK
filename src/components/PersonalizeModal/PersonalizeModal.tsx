import React from 'react';
import './PersonalizeModal.css';

interface PersonalizeModalProps {
  isOpen: boolean;
  onClose: () => void;
  content: string;
  reasoning?: string;
  error?: string | null;
  processingTime?: number | null;
}

const PersonalizeModal: React.FC<PersonalizeModalProps> = ({
  isOpen,
  onClose,
  content,
  reasoning,
  error,
  processingTime
}) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">Personalized Content</h3>
          <button className="modal-close-button" onClick={onClose} aria-label="Close">
            &times;
          </button>
        </div>

        <div className="modal-body">
          {error ? (
            <div className="error-container">
              <h4 className="error-title">Error</h4>
              <p className="error-message">{error}</p>
            </div>
          ) : (
            <>
              {reasoning && (
                <div className="personalization-reasoning">
                  <h4>Why this content:</h4>
                  <p>{reasoning}</p>
                </div>
              )}

              {processingTime !== null && processingTime !== undefined && (
                <div className="processing-info">
                  <small>Processed in {processingTime}ms</small>
                </div>
              )}

              <div className="personalized-content">
                <h4>Personalized for you:</h4>
                <div className="content-text">
                  {content ? (
                    <p>{content}</p>
                  ) : (
                    <p>No personalized content available.</p>
                  )}
                </div>
              </div>
            </>
          )}
        </div>

        <div className="modal-footer">
          <button className="modal-close-button secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default PersonalizeModal;