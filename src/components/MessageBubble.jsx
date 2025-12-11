import React from 'react';

const MessageBubble = ({ text, sender, sources, error, timestamp }) => {
  const isUser = sender === 'user';

  return (
    <div className={`chatbot-message ${sender}-message`}>
      <div className="message-content">
        {error ? (
          <p style={{ color: '#ff6b6b' }}>{text}</p>
        ) : (
          <p>{text}</p>
        )}
        {sources && sources.length > 0 && (
          <div className="message-sources">
            <small>Sources:</small>
            <ul>
              {sources.slice(0, 3).map((source, index) => (
                <li key={index}>
                  <a href={source.url} target="_blank" rel="noopener noreferrer">
                    {source.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;