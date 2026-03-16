# ✨ Skincare AI Assistant

## Project Overview

The **Skincare AI Assistant** is a multi-agent chatbot designed to help users with skincare questions, dermatology information, and skincare product analysis.

The system integrates modern AI tools, vector databases, and multiple specialized agents to provide intelligent responses.

This project demonstrates:

* Multi-agent AI architecture
* Retrieval Augmented Generation (RAG)
* OCR image analysis
* Web search grounding
* Vector database retrieval
* LangSmith tracing

---

# 🚀 Features

### 1️⃣ Skincare Advice Agent

Provides personalized skincare guidance based on user questions.

Example:

* Acne treatment advice
* Skincare routine suggestions
* Ingredient explanations

---

### 2️⃣ Skin Type Detection

Users answer questions about their skin and the system predicts their skin type.

---

### 3️⃣ Web Search Agent

Uses internet search to retrieve real-time skincare information.

---

### 4️⃣ Document Q&A (RAG)

Users can upload skincare PDFs and ask questions about them.

Pipeline:

PDF → Text Chunking → Embeddings → FAISS Vector Database → Retrieval → AI Answer

---

### 5️⃣ Dermatologist Finder

Finds dermatologists in selected cities.

Displays:

* Doctor Name
* Clinic
* Address
* Phone
* Google Maps Link

---

### 6️⃣ Ingredient Scanner (OCR)

Users upload skincare product images.

Pipeline:

Image → OCR → Ingredient Extraction → AI Analysis

---

# 🧠 System Architecture

Frontend:
Streamlit Chat Interface

Backend:
Python + LangChain Agents

Database:
FAISS Vector Database

AI Model:
OpenAI LLM

Monitoring:
LangSmith Tracing

---

# 📁 Project Structure

```
skincare_chatbot
│
├── frontend
│   └── app.py
│
├── backend
│   ├── agents
│   │   ├── skincare_agent.py
│   │   ├── search_agent.py
│   │   ├── rag_agent.py
│   │   ├── doctor_agent.py
│   │   ├── ocr_agent.py
│   │   └── skintype_agent.py
│   │
│   ├── db
│   │   └── vector_store.py
│   │
│   └── utils
│       └── pdf_loader.py
│
└── requirements.txt
```

---

# ⚙️ Installation

Clone the repository:

```
git clone https://github.com/yourusername/skincare-ai-chatbot.git
```

Move into the folder:

```
cd skincare-ai-chatbot
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Start the Streamlit interface:

```
streamlit run frontend/app.py
```

The chatbot will open in your browser.

---

# 🔍 LangSmith Tracing

LangSmith is used to monitor and trace agent execution.

Set environment variables in `.env`:

```
OPENAI_API_KEY=your_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=skincare_chatbot
```

LangSmith Dashboard:

https://smith.langchain.com

---

# 🎥 Project Demonstration

The project demonstration video includes:

1. Full chatbot functionality demo
2. Agent architecture explanation
3. Code walkthrough

---

# 📌 Technologies Used

* Python
* Streamlit
* LangChain
* OpenAI
* FAISS Vector Database
* OCR
* Google Search API
* LangSmith
