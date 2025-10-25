import React, { useState } from "react";
import axios from "axios";

const BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

export default function UploadFile({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF file");
    try {
      setLoading(true);
      setMessage("Uploading and processing...");
      const formData = new FormData();
      formData.append("file", file);

      // 1️⃣ Upload the file
      await axios.post(`${BASE_URL}/upload`, formData);

      // 2️⃣ Extract text
      const fileName = file.name.replace(".pdf", "");
      await axios.post(`${BASE_URL}/extract_text?filename=${fileName}`);

      setMessage("✅ File processed successfully!");
      onUploadSuccess(fileName);
    } catch (err) {
      console.error(err);
      setMessage("❌ Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-3 shadow-sm mb-3">
      <h5>📄 Upload Legal Document</h5>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="form-control mb-2"
      />
      <button
        className="btn btn-primary w-100"
        onClick={handleUpload}
        disabled={loading}
      >
        {loading ? "Processing..." : "Upload & Extract"}
      </button>
      {message && <p className="mt-2 text-center">{message}</p>}
    </div>
  );
}