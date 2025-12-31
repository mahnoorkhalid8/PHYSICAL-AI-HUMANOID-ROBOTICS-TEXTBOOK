import React, { useEffect, useState } from 'react';
import './styles.css';

interface TranslateModalProps {
  isOpen: boolean;
  onClose: () => void;
  originalContent: string;
  translatedContent: string;
  error?: string | null;
  processingTime?: number;
}

const TranslateModal: React.FC<TranslateModalProps> = ({
  isOpen,
  onClose,
  originalContent,
  translatedContent,
  error,
  processingTime
}) => {
  const [viewMode, setViewMode] = useState<'original' | 'translated' | 'side-by-side'>('translated');
  const [rtlContent, setRtlContent] = useState<string>('');

  useEffect(() => {
    if (translatedContent) {
      // Process the translated content to ensure proper RTL rendering
      setRtlContent(translatedContent);
    }
  }, [translatedContent]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Urdu Translation</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        {error ? (
          <div className="modal-error">
            <p>Error: {error}</p>
          </div>
        ) : (
          <>
            <div className="modal-controls">
              <button
                className={viewMode === 'original' ? 'active' : ''}
                onClick={() => setViewMode('original')}
              >
                Original
              </button>
              <button
                className={viewMode === 'translated' ? 'active' : ''}
                onClick={() => setViewMode('translated')}
              >
                Translated
              </button>
              <button
                className={viewMode === 'side-by-side' ? 'active' : ''}
                onClick={() => setViewMode('side-by-side')}
              >
                Side-by-Side
              </button>
            </div>

            <div className="modal-body">
              {viewMode === 'original' && (
                <div className="content-section original-content">
                  <h3>Original Content</h3>
                  <div className="content-display">{originalContent}</div>
                </div>
              )}

              {viewMode === 'translated' && (
                <div className="content-section translated-content">
                  <h3>Translated Content (Urdu)</h3>
                  <div className="content-display urdu-content" dir="rtl">
                    {rtlContent}
                  </div>
                </div>
              )}

              {viewMode === 'side-by-side' && (
                <div className="side-by-side-container">
                  <div className="content-section original-content half-width">
                    <h3>Original</h3>
                    <div className="content-display">{originalContent}</div>
                  </div>
                  <div className="content-section translated-content half-width">
                    <h3>Urdu Translation</h3>
                    <div className="content-display urdu-content" dir="rtl">
                      {rtlContent}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {processingTime && (
              <div className="modal-footer">
                <p>Processing time: {processingTime}ms</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default TranslateModal;