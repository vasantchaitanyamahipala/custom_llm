import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import logo from "./image.png"; 

function App() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!userInput.trim()) return;

    const newMessage = { role: "user", content: userInput };
    setMessages((prev) => [...prev, newMessage]);

    try {
      const response = await axios.post("http://127.0.0.1:8000/chat", {
        message: userInput,
      });

      const botMessage = { role: "assistant", content: response.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { role: "assistant", content: "Error: Unable to fetch response." };
      setMessages((prev) => [...prev, errorMessage]);
    }

    setUserInput("");
  };

  return (
    <div className="container">
      <header className="header">
        <img src={logo} alt="Arbor Logo" className="logo" />
      </header>
      <div className="chat-container">
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.role === "user" ? "user-message" : "bot-message"}`}
            >
              {msg.content}
            </div>
          ))}
        </div>
        <form className="chat-input" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Type your message..."
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
          />
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
}

export default App;