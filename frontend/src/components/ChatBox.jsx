import React from "react";

export default function ChatBox({ messages }) {
  return (
    <div
      className="border p-3 mb-3"
      style={{ height: "400px", overflowY: "auto", background: "#f9f9f9" }}
    >
      {messages.length === 0 ? (
        <p className="text-muted text-center">No conversation yet.</p>
      ) : (
        messages.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-2 ${
              msg.sender === "user" ? "text-end" : "text-start"
            }`}
          >
            <span
              className={`badge ${
                msg.sender === "user" ? "bg-primary" : "bg-secondary"
              }`}
            >
              {msg.sender === "user" ? "You" : "LegalAI"}
            </span>
            <div className="p-2 mt-1 border rounded bg-white">{msg.text}</div>
          </div>
        ))
      )}
    </div>
  );
}