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

  const [sessionId, setSessionId] = useState(() => {
    // Try to get session ID from localStorage (only in browser)
    if (typeof window !== 'undefined') {
      return localStorage.getItem('chatbot-session-id') || null;
    }
    return null;
  });

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

      // For now, since there's no backend, return a mock response
      // In a real implementation, you would have a backend service to handle this
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network delay

      const mockResponse = {
        answer: "Thanks for your message! This is a frontend-only version of the chatbot. In a full implementation, this would connect to a backend API to provide AI-powered responses based on the textbook content.",
        sources: []
      };

      // Add bot response to the chat
      const botMessage = {
        id: Date.now() + 1,
        text: mockResponse.answer,
        sender: 'bot',
        sources: mockResponse.sources || [],
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