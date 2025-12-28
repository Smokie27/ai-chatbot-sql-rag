# AI Financial Chatbot (SQL + RAG)

An **AI-powered financial chatbot** that answers business questions by combining **SQL analytics** with **document-based reasoning (RAG)** and **automatic visualizations** — all running **locally and free**.

---

## What It Does

* Ask questions in **plain English**
* Automatically generates and runs **safe SQL queries**
* Answers **contextual questions from PDFs** (annual reports, strategy docs)
* **Combines numbers + explanations** in a single response
* Generates **bar and line charts** automatically
* Interactive **web UI** using Streamlit

---

## How It Works (In One View)

```
User Question
   ↓
Streamlit UI
   ↓
Decision Layer
 ─ SQL Engine (MySQL) → numbers
 ─ RAG Engine (FAISS + PDFs) → context
   ↓
LLM (LLaMA 3)
   ↓
Answer + Table + Chart
```

---

## Tech Stack

* **Frontend:** Streamlit
* **Database:** MySQL
* **LLM:** LLaMA 3 (Ollama, local)
* **Embeddings:** HuggingFace MiniLM
* **Vector DB:** FAISS
* **Language:** Python

---

## Key Design Features

* SELECT-only SQL guardrails (no data modification)
* Grounded answers (no hallucinated explanations)
* Charts generated only when data shape is valid
* Fully local, no paid APIs

---

## Why This Project Is Strong

* Demonstrates **real AI system design**, not a notebook demo
* Integrates **structured + unstructured data**
* Uses **production-style RAG architecture**
* Shows **analytics + AI + product thinking**
* Runs **locally**
---

