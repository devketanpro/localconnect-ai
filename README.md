# 🧠 Smart Local Discovery Chatbot

A conversational chatbot that helps users discover local services, events, and general information using natural language queries.

---

## 🌐 Features

- 🔍 Understands and processes queries like:
  - `Top schools in Indore`
  - `Vegetarian restaurants near MG Road, Bengaluru`
  - `What is Python?`

- ✅ Intelligent query classification:
  - General knowledge → Wikipedia
  - Location-based queries → DuckDuckGo API (with fallback to mock data)
  - Custom knowledge base → Predefined mock data

- 💬 Frontend built with **Streamlit** for interactive chat UI  
- ⚡ FastAPI backend with `/search` endpoint  
- ⛑ Mock data fallback when live APIs fail

---

## 🛠️ Tech Stack

| Layer       | Tech Used                                |
|-------------|------------------------------------------|
| Backend     | FastAPI, Pydantic                        |
| Frontend    | Streamlit                                |
| APIs        | DuckDuckGo Instant Answer API, Wikipedia REST API |
| Fallback    | Python mock data (`mock_data.py`)        |
| Others      | `requests`, `dotenv`, `uvicorn`          |

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt

Built for the **LocalConnect AI Task Assignment**  
By: _Gourav Sharma_
