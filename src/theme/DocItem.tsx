import React from 'react';
import { useLocation } from '@docusaurus/router';
import AuthGuard from '@site/src/components/AuthGuard';
import OriginalDocItem from '@theme-original/DocItem';
import PersonalizeButton from '@site/src/components/PersonalizeButton/PersonalizeButton';

const ProtectedDocItem = (props) => {
  const location = useLocation();

  // Protect all doc pages that are part of the book content
  const isBookContent = location.pathname.startsWith('/docs/');

  if (isBookContent) {
    // For book content, wrap with auth guard and add personalized button at the top
    return (
      <AuthGuard redirectTo="/sign-in">
        <div>
          {/* Personalize Button at the top */}
          <div style={{
            position: 'relative',
            margin: '20px 0',
            padding: '15px',
            backgroundColor: '#f8f9fa',
            borderRadius: '8px',
            border: '2px solid #e9ecef',
            maxWidth: '100%',
            textAlign: 'left',
            zIndex: 1000,
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            marginBottom: '30px'
          }} className="personalize-section">
            <h3 style={{ margin: '0 0 10px 0', color: '#495057' }}>Personalize This Content</h3>
            <div style={{ marginBottom: '10px' }}>
              <PersonalizeButton
                chapterContent={'Current chapter content'}
                chapterTitle={location.pathname.split('/').pop() || 'Current Chapter'}
              />
            </div>
            <p style={{ margin: '10px 0 0 0', fontSize: '0.9em', color: '#6c757d', maxWidth: '600px' }}>
              Get content tailored to your hardware and software background
            </p>
          </div>

          <OriginalDocItem {...props} />
        </div>
      </AuthGuard>
    );
  }

  // For non-book content pages, show without auth
  return <OriginalDocItem {...props} />;
};

export default ProtectedDocItem;