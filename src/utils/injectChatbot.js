import React from 'react';
import { createRoot } from 'react-dom/client';
import ChatbotWidget from '../components/ChatbotWidget';

// Wait for the DOM to be ready before injecting the chatbot
function injectChatbot() {
  // Create a container for the chatbot
  const chatbotContainer = document.createElement('div');
  chatbotContainer.id = 'chatbot-container';
  document.body.appendChild(chatbotContainer);

  // Render the chatbot widget
  const root = createRoot(chatbotContainer);
  root.render(React.createElement(ChatbotWidget));
}

// Check if the DOM is already loaded
if (document.readyState === 'loading') {
  // If still loading, wait for DOMContentLoaded
  document.addEventListener('DOMContentLoaded', injectChatbot);
} else {
  // If already loaded, inject immediately
  injectChatbot();
}