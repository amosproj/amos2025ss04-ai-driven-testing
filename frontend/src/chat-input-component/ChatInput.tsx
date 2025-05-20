import React, { useState } from 'react';
import './ChatInput.css';

type ChatInputProps = {
  onSend: (message: string) => void;
};

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) return;

    onSend(input);
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="chat-input-form">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
        className="chat-textarea"
      />
      <button type="submit" className="chat-button">
        Send
      </button>
    </form>
  );
};

export default ChatInput;
