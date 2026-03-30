# legalai
Full-stack Generative AI app that simplifies and analyzes legal documents using NLP and RAG. Upload contracts, get AI-generated summaries, risk insights, and chat-based explanations. Built with React, FastAPI, and open-source models.


# README – Frontend (Vite + React)

## 🚀 How to Run the Frontend

### 1️⃣ Navigate to the frontend folder

```bash
cd frontend
```

### 2️⃣ Install dependencies

```bash
npm install
```

### 3️⃣ Start the development server

```bash
npm run dev
```

### ✔ Expected Output

```
VITE vX.X.X  ready in XXX ms
➜  Local:   http://localhost:5173/
```

Open the browser and visit:
👉 **[http://localhost:5173/](http://localhost:5173/)**

---

# README – Backend (FastAPI)

## ⚙️ How to Run the Backend

### 1️⃣ Navigate to backend folder

```bash
cd backend
```

### 2️⃣ Create & activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run FastAPI server

```bash
uvicorn app.main:app --reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # Listen on all network interfaces.
```

### ✔ Expected Output

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Open API Docs

👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**



