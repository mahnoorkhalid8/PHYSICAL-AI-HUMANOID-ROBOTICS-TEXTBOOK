import React from 'react';

const LoadingIndicator = () => {
  return (
    <div className="chatbot-message bot-message">
      <div className="message-content">
        <div className="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  );
};

export default LoadingIndicator;