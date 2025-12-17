import React from 'react';

// A blank page for the chatbot route
// The chatbot is injected globally via client modules in docusaurus.config.ts
function ChatbotGlobalPage() {
  return (
    <div>
      <h1>Chatbot</h1>
      <p>The chatbot is available globally on this site.</p>
    </div>
  );
}

export default ChatbotGlobalPage;