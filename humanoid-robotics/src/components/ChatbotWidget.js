import React, { useState } from 'react';
import styles from './ChatbotWidget.module.css'; // Assuming a CSS module for styling

const ChatbotWidget = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // You might want to get this from Docusaurus config or an environment variable
  const RAG_BACKEND_URL = process.env.NODE_ENV === 'production'
    ? 'https://your-production-backend.com'
    : 'http://localhost:8000'; // Default for local development

  const handleSendMessage = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setResponse(null);
    setError(null);

    try {
      const res = await fetch(`${RAG_BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Something went wrong');
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <h3>Ask the AI Textbook</h3>
      <div className={styles.chatWindow}>
        {loading && <p>Loading...</p>}
        {error && <p className={styles.error}>Error: {error}</p>}
        {response && (
          <div>
            <p>{response.response}</p>
            {response.source_urls && response.source_urls.length > 0 && (
              <div>
                <strong>Sources:</strong>
                <ul>
                  {response.source_urls.map((url, index) => (
                    <li key={index}><a href={url} target="_blank" rel="noopener noreferrer">{url.split('/').pop()}</a></li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
      <div className={styles.chatInput}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSendMessage();
            }
          }}
          placeholder="Type your question..."
          disabled={loading}
        />
        <button onClick={handleSendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatbotWidget;
