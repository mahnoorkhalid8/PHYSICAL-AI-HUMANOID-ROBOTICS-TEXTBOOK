import React, { useState } from 'react';

const MessageInput = ({ onSendMessage, isLoading }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSendMessage = () => {
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chatbot-input-area">
      <textarea
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question about the textbook..."
        className="chatbot-input"
        disabled={isLoading}
        rows="1"
      />
      <button
        onClick={handleSendMessage}
        disabled={!inputValue.trim() || isLoading}
        className="chatbot-send-btn"
      >
        {isLoading ? 'Sending...' : 'Send'}
      </button>
    </div>
  );
};

export default MessageInput;