// ChatBot.js

import React, {useState} from 'react';
import './ChatBot.css';

const ChatBot = ({ sendMessage }) => {

  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(Date())
    changeSubmit()
  };

  const changeSubmit = async() => {
    const data = {message};
    try {
      const response = await fetch('/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      const responseData = await response.json();
      console.log(responseData)
      setResponse(responseData.result);
      console.log(Date())
    } catch (error) {
      console.error('Error:', error);
    }
    
  }

  return (
    <div className="chat-bot">
      <form classNam e= "inputForm" onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={handleChange}
          placeholder="Type your message here..."
          required
        />
        <button type="submit">Send</button>
        <p className='result'>{response}</p>
      </form>
      
    </div>
  );
};

export default ChatBot;
