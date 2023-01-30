import React, { useState, useEffect } from 'react';
import './ChatWindow.css';

const ChatWindow = () => {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        fetch('messagesData.json')
            .then(response => response.json())
            .then(data => setMessages(data));
    }, []);

    return (
        <div className="chat-window">
            {messages.map((message, i) => (
                <div key={i} className={`message ${message.isUser ? 'user' : 'bot'}`}>
                    {message.message}
                </div>
            ))}
        </div>
    );
};

export default ChatWindow;
