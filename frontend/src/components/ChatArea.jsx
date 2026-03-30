import React from "react";
import MessageBubble from "./MessageBubble";
import "./ChatArea.css";

function ChatArea({
  chatContainerRef,
  messages,
  loading,
  uploading,
  fileInputRef,
  handleFileSelect,
  editingIndex,
  editingText,
  setEditingIndex,
  setEditingText,
  handleSaveEdit,
  handleCopy,
  handleRegenerate,
  messagesEndRef,
  messageLoading,
}) {
  return (
    <div ref={chatContainerRef} className="tidio-chat-area">
      {uploading || messageLoading ? (
        <div className="center-loading">
          <div className="spinner"></div>
          <p>Processing document...</p>
        </div>
      ) : (
        <div className="messages-container">
          {messages.map((msg, idx) => (
            <MessageBubble
              key={idx}
              msg={msg}
              idx={idx}
              editingIndex={editingIndex}
              editingText={editingText}
              setEditingIndex={setEditingIndex}
              setEditingText={setEditingText}
              handleSaveEdit={handleSaveEdit}
              handleCopy={handleCopy}
              handleRegenerate={handleRegenerate}
            />
          ))}

          {loading && (
            <div className="message message-ai">
              <div className="message-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"
                  />
                </svg>
              </div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          {uploading && (
            <div className="message message-ai">
              <div className="message-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"
                  />
                </svg>
              </div>
              <div className="message-content">
                <div className="message-bubble">
                  <div className="uploading-indicator-inline">
                    <div className="spinner-small"></div>
                    <span>Processing your document...</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
}

export default ChatArea;
