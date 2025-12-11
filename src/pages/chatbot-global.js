import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';
import ChatbotWidget from '../components/ChatbotWidget';

if (ExecutionEnvironment.canUseDOM) {
  // Create a container for the chatbot
  const chatbotContainer = document.createElement('div');
  chatbotContainer.id = 'global-chatbot-container';
  document.body.appendChild(chatbotContainer);

  // Dynamically render the chatbot widget using React
  // This requires importing React and ReactDOM dynamically
  const renderChatbot = async () => {
    const React = (await import('react')).default;
    const ReactDOM = (await import('react-dom/client')).default;

    const root = ReactDOM.createRoot(chatbotContainer);
    root.render(React.createElement(ChatbotWidget));
  };

  // Wait for the page to load before rendering
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderChatbot);
  } else {
    renderChatbot();
  }
}