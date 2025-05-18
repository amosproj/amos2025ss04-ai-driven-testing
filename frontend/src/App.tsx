import React from 'react';
import logo from './logo.svg';
import ChatInput from './chat-input-component/ChatInput';

import './App.css';

const App: React.FC = () => {
  const handleSendMessage = (message: string) => {
    console.log('Message sent:', message);
    // Later: send to your chatbot backend or display it in UI
  };

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">AMOS LLM </h1>
      <ChatInput onSend={handleSendMessage} />
    </div>
  );
};

export default App;
