import React from "react";
import "./App.css";
import Header from "./components/Header";
import ChatArea from "./components/ChatArea";
import InputArea from "./components/InputArea";
import NewChatModal from "./components/NewChatModal";
import useChatLogic from "./hooks/useChatLogic";

function App() {
  const {
    theme,
    toggleTheme,
    fileName,
    messages,
    question,
    setQuestion,
    loading,
    uploading,
    showNewChatModal,
    setShowNewChatModal,
    menuOpen,
    setMenuOpen,
    isStreaming,
    editingIndex,
    setEditingIndex,
    editingText,
    setEditingText,
    toastMessage,
    fileInputRef,
    menuRef,
    menuButtonRef,
    chatContainerRef,
    messagesEndRef,
    handleFileSelect,
    handleNewChat,
    handleSaveEdit,
    handleRegenerate,
    handleCopy,
    handleAsk,
    stopStreamingRef,
  } = useChatLogic();

  return (
    <div className="tidio-container">
      <Header
        theme={theme}
        toggleTheme={toggleTheme}
        fileName={fileName}
        messages={messages}
        menuOpen={menuOpen}
        setMenuOpen={setMenuOpen}
        menuButtonRef={menuButtonRef}
        menuRef={menuRef}
        handleNewChat={handleNewChat}
      />

      <ChatArea
        chatContainerRef={chatContainerRef}
        messages={messages}
        loading={loading}
        uploading={uploading}
        fileInputRef={fileInputRef}
        handleFileSelect={handleFileSelect}
        editingIndex={editingIndex}
        editingText={editingText}
        setEditingIndex={setEditingIndex}
        setEditingText={setEditingText}
        handleSaveEdit={handleSaveEdit}
        handleCopy={handleCopy}
        handleRegenerate={handleRegenerate}
        messagesEndRef={messagesEndRef}
      />

      <InputArea
        fileName={fileName}
        messages={messages}
        question={question}
        setQuestion={setQuestion}
        loading={loading}
        uploading={uploading}
        isStreaming={isStreaming}
        setShowNewChatModal={setShowNewChatModal}
        handleAsk={handleAsk}
        fileInputRef={fileInputRef}
        handleFileSelect={handleFileSelect}
        stopStreamingRef={stopStreamingRef}
      />

      {showNewChatModal && (
        <NewChatModal
          fileName={fileName}
          setShowNewChatModal={setShowNewChatModal}
          handleNewChat={handleNewChat}
          fileInputRef={fileInputRef}
        />
      )}

      {toastMessage && (
        <div className="toast-notification">
          {toastMessage}
        </div>
      )}
    </div>
  );
}

export default App;