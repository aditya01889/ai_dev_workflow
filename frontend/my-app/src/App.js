import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [logs, setLogs] = useState([]);

    const handleSendMessage = async () => {
        if (input.trim() !== "") {
            const newMessage = { user: "User", text: input };
            setMessages([...messages, newMessage]);
            setInput("");

            // Send message to backend
            await axios.post('/api/gather', { text: input });
        }
    };

    const handleFinalize = async () => {
        await axios.post('/api/finalize');
    };

    const fetchLogs = async () => {
        const response = await axios.get('/api/logs');
        setLogs(response.data);
    };

    useEffect(() => {
        // Fetch logs periodically
        const interval = setInterval(fetchLogs, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="App">
            <div className="chat-window">
                <div className="messages">
                    {messages.map((message, index) => (
                        <div key={index} className="message">
                            <strong>{message.user}:</strong> {message.text}
                        </div>
                    ))}
                </div>
                <div className="input">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your requirements..."
                    />
                    <button onClick={handleSendMessage}>Send</button>
                    <button onClick={handleFinalize}>Finalize</button>
                </div>
            </div>
            <div className="preview-section">
                <h2>Preview</h2>
                <div className="preview-content">
                    {/* Add logic to display work being done/completed */}
                </div>
                <h2>Logs</h2>
                <div className="logs">
                    {logs.map((log, index) => (
                        <div key={index} className="log">
                            {log}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;
