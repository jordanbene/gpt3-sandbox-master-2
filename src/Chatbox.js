import React, { Component } from 'react';
import { ChatFeed, Message, ChatBubbleProps } from 'react-chat-ui'
import messagesData from './messagesData.json'
//import messagesData from './new_messages.json';


import axios from 'axios';
import chatbot from './chatbot.css';

  
class Chatbox extends Component {
  constructor(props) {
    super(props);
    this.state = {
      messages: []
    }
  }

  componentDidMount() {
    //this.setState({ messages: messagesData });
    const messages = messagesData.map(data => {
      return new Message({
        id: data.message.id,
        message: data.message,
        senderName: data.message.isUser === 'true' ? 'User' : 'Bot',
      });
    });
    this.setState({ messages });
    console.log("ISUSER 2:  ", messages)

  }
  
  handleNewMessage = (newMessage) => {
    this.setState({ messages: [...this.state.messages, newMessage] });
  };

  chatBubbleProps = (message) => {
    return {
      showAvatar: true,
      isOwnMessage: message.isUser === 'true',
      isFirst: true,
      isLast: true,
      position: message.isUser === 'true' ? 'right' : 'left'
    }
  }

  messageProps = (message) => {
    console.log("ISUSER:  ", message)
    if (message.isUser === 'true') {
      return {
        right: true,
        backgroundColor: '#0084ff',
        color: '#fff'
      }
    } else {
      return {
        left: true,
        backgroundColor: '#f0f0f0',
        color: '#000'
      }
    }
  }

  clearHistory = async () => {
    this.setState({ messages: [] });
    try {
      const response = await axios.post('http://localhost:5000/clear-history');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  }

  render() {
    return (
      
      <div className="chat-container">
        
        <ChatFeed
          messages={this.state.messages}
          onNewMessage={this.handleNewMessage}
          chatBubbleProps={(message, index) => this.chatBubbleProps(message, index)}
          messageProps={(message) => this.messageProps(message)}
          
        />
        
        <button className="clear-history-btn" onClick={this.clearHistory}>Clear History</button>
        
      </div>
    );
  }
  
}

export default Chatbox;
