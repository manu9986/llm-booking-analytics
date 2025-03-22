# LLM-Powered Booking Analytics & QA System

## 📌 Overview
This project is an **LLM-powered hotel booking analytics and QA system** built with **FastAPI, ChromaDB, OpenAI API, and SQLite**. It processes hotel booking data, provides precomputed analytics, and enables natural language interaction using **Retrieval-Augmented Generation (RAG)**.

## 🚀 Features
- **Data Preprocessing**: Loads, cleans, and stores hotel booking data.
- **Precomputed Analytics**: Revenue trends, cancellation rates, booking lead times.
- **RAG-based QA System**: Answers queries using OpenAI GPT-4 and ChromaDB for vector search.
- **FastAPI Endpoints**: Provides analytics data and chatbot interaction.
- **Performance Logging**: Tracks API request durations.

---

## 🛠️ Installation & Setup
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/manu9986/llm-booking-analytics.git
cd llm-booking-analytics
```

### 2️⃣ **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Set Up Environment Variables**
Create a `.env` file in the project root with:
```env
OPENAI_API_KEY=your_openai_api_key
```

### 5️⃣ **Prepare the Database**
```bash
python precompute.py  # Precompute analytics and store in SQLite
python main.py        # Embed booking data into ChromaDB
```

### 6️⃣ **Run the FastAPI Server**
```bash
uvicorn database:app --reload
```
Access API docs at: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📊 API Endpoints
### 🔹 **Analytics**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analytics/revenue` | GET | Monthly revenue trend |
| `/api/analytics/cancellations` | GET | Cancellation rate |
| `/api/analytics/geography` | GET | Booking distribution by country |
| `/api/analytics/lead_time` | GET | Histogram of booking lead times |

### 🔹 **LLM-Powered Chatbot**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask` | POST | Query the AI assistant |

**Example Query:**
```json
{
  "question": "What was the highest revenue month last year?"
}
```

**Expected Response:**
```json
{
  "answer": "The highest revenue month was December 2023 with $125,000."
}
```

---

## 🔬 Sample Test Queries & Expected Answers
| Query | Expected Answer |
|----------|-----------------|
| "What is the average cancellation rate?" | "The cancellation rate is 18.5%." |
| "Which country has the most bookings?" | "The most bookings come from Portugal (25%)." |

---

## 📑 Implementation Details
- **ChromaDB** is used for **vector search** on booking data.
- **OpenAI API** provides natural language responses.
- **FastAPI** manages the backend for analytics & QA.
- **Precomputed analytics** ensure fast API responses.

### ❗ Challenges & Solutions
1. **Handling Large Datasets** → Used SQLite indexing & ChromaDB for fast retrieval.
2. **Enhancing Response Accuracy** → Implemented RAG with top-5 document retrieval.
3. **Optimizing API Latency** → Precomputed analytics instead of real-time computation.

---

## 📌 Future Improvements
- **Hybrid Search (BM25 + embeddings)** for better accuracy.
- **Authentication & Rate Limiting** to prevent API abuse.
- **Real-time ChromaDB Updates** when new booking data is added.

---

## 📜 License
This project is licensed under the MIT License.

---

## ⭐ Contributing
Contributions are welcome! Feel free to open issues and submit pull requests.

---

## 📬 Contact
For any questions, reach out to **manugowda6160@gmail.com**.

