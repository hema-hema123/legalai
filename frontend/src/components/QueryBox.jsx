import React, { useState } from "react";
import axios from "axios";

const BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

export default function QueryBox({ fileName, onNewMessage }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question) return;
    setLoading(true);
    onNewMessage({ sender: "user", text: question });

    try {
      const res = await axios.post(
        `${BASE_URL}/ai_answer`,
        {
          index_name: fileName,
          question: question,
          top_k: 3,
        }
      );

      const answer = res.data.answer || "No answer received.";
      onNewMessage({ sender: "ai", text: answer });
    } catch (err) {
      console.error(err);
      onNewMessage({ sender: "ai", text: "❌ Failed to fetch answer." });
    } finally {
      setQuestion("");
      setLoading(false);
    }
  };

  return (
    <div className="input-group mt-3">
      <input
        type="text"
        className="form-control"
        placeholder="Ask a legal question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleAsk()}
      />
      <button
        className="btn btn-success"
        onClick={handleAsk}
        disabled={loading}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>
    </div>
  );
}