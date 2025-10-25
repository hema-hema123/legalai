import React, { useState } from "react";
import UploadFile from "./components/UploadFile";
import QueryBox from "./components/QueryBox";
import ChatBox from "./components/ChatBox";


function App() {
  const [fileName, setFileName] = useState(null);
  const [messages, setMessages] = useState([]);

  const handleUploadSuccess = (name) => setFileName(name);

  const handleNewMessage = (msg) => setMessages((prev) => [...prev, msg]);

  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">⚖️ LegalAI Assistant</h2>
      <UploadFile onUploadSuccess={handleUploadSuccess} />
      {fileName && <p className="text-success">Using file: {fileName}</p>}
      <ChatBox messages={messages} />
      {fileName && <QueryBox fileName={fileName} onNewMessage={handleNewMessage} />}
    </div>
  );
}

export default App;