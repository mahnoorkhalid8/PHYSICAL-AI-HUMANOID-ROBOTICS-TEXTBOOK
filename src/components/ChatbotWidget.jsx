import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import MessageInput from './MessageInput';
import LoadingIndicator from './LoadingIndicator';
import './ChatbotWidget.css'; // We'll create this CSS file for the black-gold theme

const ChatbotWidget = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const [sessionId, setSessionId] = useState(null);

  // Initialize session ID from localStorage when component mounts
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedSessionId = localStorage.getItem('chatbot-session-id');
      if (storedSessionId) {
        setSessionId(storedSessionId);
      }
    }
  }, []);

  const handleSendMessage = async (text) => {
    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      text: text,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Get selected text if any (check if running in browser)
      const selectedText = typeof window !== 'undefined' && window.getSelection ? window.getSelection().toString().trim() : '';

      // Prepare the request payload
      const requestBody = {
        question: text,
      };

      // Add session ID if we have one
      if (sessionId) {
        requestBody.session_id = sessionId;
      }

      // Add selected text if there's any
      if (selectedText) {
        requestBody.selected_text = selectedText;
        requestBody.context = {
          page_url: typeof window !== 'undefined' ? window.location.pathname : '',
          search_scope: 'selected_text'
        };
      } else {
        requestBody.context = {
          page_url: typeof window !== 'undefined' ? window.location.pathname : '',
          search_scope: 'full_book'
        };
      }

      // Use backend API endpoint
      // For development, use the backend server directly
      // For production, this will be proxied through Vercel
      const apiEndpoint = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
        ? '/api/query'  // Use relative path in production
        : 'http://localhost:8000/api/query';  // Direct backend URL in development

      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      let data;

      // If the response is not OK, try to read the error details from the body
      if (!response.ok) {
        let errBody = null;
        try {
          errBody = await response.json();
        } catch (e) {
          // ignore JSON parse errors and create a generic error
          errBody = { detail: { error: `API request failed with status ${response.status}` } };
        }

        let errMsg = `API request failed with status ${response.status}`;
        let error_code = '';
        if (errBody) {
          if (errBody.detail) {
            if (typeof errBody.detail === 'string') {
              errMsg = errBody.detail;
            } else if (errBody.detail.error) {
              errMsg = `${errBody.detail.error}${errBody.detail.details?.message ? `: ${errBody.detail.details.message}` : ''}`;
              error_code = errBody.detail.error;
            } else if (errBody.detail.message) {
              errMsg = errBody.detail.message;
            }
          } else if (errBody.error) {
            errMsg = errBody.error;
            error_code = errBody.error;
          }
        }

        // If it's a SESSION_NOT_FOUND error, clear the invalid session ID
        if (error_code === 'SESSION_NOT_FOUND' || errMsg.includes('SESSION_NOT_FOUND')) {
          localStorage.removeItem('chatbot-session-id');
          setSessionId(null);
          // Don't throw an error, just continue without the session ID
          // The backend will create a new session automatically
          // Return early to avoid trying to parse the response again
          return;
        } else {
          throw new Error(errMsg);
        }
      } else {
        // Only parse the JSON if the response is OK
        data = await response.json();
      }

      // If a new session ID was returned, store it
      if (data.session_id) {
        setSessionId(data.session_id);
        localStorage.setItem('chatbot-session-id', data.session_id);
      }

      // Add bot response to the chat
      const botMessage = {
        id: Date.now() + 1,
        text: data.answer,
        sender: 'bot',
        sources: data.sources || [],
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        text: error?.message ? `Sorry, ${error.message}` : 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        error: true,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="chatbot-widget">
      {isOpen ? (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <h3>Textbook Assistant</h3>
            <button className="chatbot-close-btn" onClick={toggleChat}>
              ×
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your textbook assistant. Ask me about the Physical AI Humanoid Robotics content.</p>
              </div>
            ) : (
              messages.map((message) => (
                <MessageBubble
                  key={message.id}
                  text={message.text}
                  sender={message.sender}
                  sources={message.sources}
                  error={message.error}
                  timestamp={message.timestamp}
                />
              ))
            )}
            {isLoading && <LoadingIndicator />}
            <div ref={messagesEndRef} />
          </div>

          <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      ) : (
        <button className="chatbot-toggle-btn" onClick={toggleChat}>
          💬
        </button>
      )}
    </div>
  );
};

export default ChatbotWidget;