// App.js
import React from 'react';
import ChatBot from './components/ChatBot.js';
import './App.css';

const App = () => {
  const sendMessage = (message) => {
  console.log('Sending message:', message);
  };

  return (
    <div className="app">
      <h1>Marketrix Chatbot</h1>
      <ChatBot sendMessage={sendMessage} />
    </div>
  );
};

export default App;
