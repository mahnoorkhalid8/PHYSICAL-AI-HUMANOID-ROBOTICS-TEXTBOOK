import React, { useEffect, useState } from 'react';
import { useLocation } from '@docusaurus/router';
import AuthGuard from '@site/src/components/AuthGuard';
import OriginalDocItem from '@theme-original/DocItem';
import PersonalizeButton from '@site/src/components/PersonalizeButton/PersonalizeButton';
import TranslateButton from '@site/src/components/TranslateButton/TranslateButton';

const ProtectedDocItem = (props) => {
  const location = useLocation();
  const [documentContent, setDocumentContent] = useState('');

  // Protect all doc pages that are part of the book content
  const isBookContent = location.pathname.startsWith('/docs/');

  // Extract document content when component mounts or location changes
  useEffect(() => {
    if (isBookContent) {
      // Extract content from the document after it's rendered
      const extractContent = () => {
        // Try multiple selectors to find the main content area of the document
        const selectors = [
          'article div[class*="markdown"]',
          'article div[class*="docItem"]',
          'article div[class*="content"]',
          'article div[class*="container"]',
          'article div[class*="main"]',
          'article',
          'main',
          '[role="main"]',
          '[class*="docContent"]'
        ];

        for (const selector of selectors) {
          const element = document.querySelector(selector);
          if (element) {
            // Extract text content, but try to get more meaningful content
            const content = element.textContent || element.innerText;
            if (content && content.trim().length > 50) { // Only set if we get meaningful content
              setDocumentContent(content.trim());
              return;
            }
          }
        }

        // If no specific content found, try to get content from the entire document body
        setDocumentContent(document.title + ' ' + (document.body.textContent || document.body.innerText));
      };

      // Try to extract content immediately and then again after a delay
      extractContent();
      const timer = setTimeout(extractContent, 500); // Try again after 500ms

      // Also try to extract content when the document is fully loaded
      const loadHandler = () => setTimeout(extractContent, 100);
      window.addEventListener('load', loadHandler);

      return () => {
        clearTimeout(timer);
        window.removeEventListener('load', loadHandler);
      };
    }
  }, [isBookContent, location.pathname]);

  if (isBookContent) {
    // For book content, wrap with auth guard and add personalized button at the top
    return (
      <AuthGuard redirectTo="/sign-in">
        <div>
          {/* Translation and Personalize Buttons at the top */}
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
          }} className="feature-buttons-section">
            <h3 style={{ margin: '0 0 10px 0', color: '#495057' }}>Enhance Your Learning</h3>
            <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap', marginBottom: '10px' }}>
              <TranslateButton
                chapterContent={documentContent}
                chapterTitle={location.pathname.split('/').pop() || 'Current Chapter'}
              />
              <PersonalizeButton
                chapterContent={documentContent}
                chapterTitle={location.pathname.split('/').pop() || 'Current Chapter'}
              />
            </div>
            <p style={{ margin: '10px 0 0 0', fontSize: '0.9em', color: '#6c757d', maxWidth: '600px' }}>
              Translate to Urdu or get content tailored to your background
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