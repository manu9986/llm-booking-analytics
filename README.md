# LLM-Powered Booking Analytics & QA System

This project provides an analytics and QA system for hotel booking data using FastAPI, SQLite, ChromaDB, and OpenAI.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/llm_booking_analytics.git
   cd llm_booking_analytics
Create a virtual environment and install dependencies:

Copy
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the project root with your OpenAI API key:
Copy
OPENAI_API_KEY=your_openai_api_key_here
Precompute Analytics Data:

Run the precompute script to generate analytics data:
Copy
python scripts/precompute.py
Run the application:

Copy
uvicorn app.main\:app --reload
Usage
API Endpoints:

GET /: Welcome message.
POST /ask: Accepts a question and returns an answer using the RAG system.
POST /api/analytics: Generates analytics reports based on the requested type and format.
Sample Test Queries:

Query: What is the revenue trend over time?
Expected Response: An image showing the revenue trends.
Query: What is the cancellation rate?
Expected Response: A JSON object with the cancellation rate.
Project Structure
app/: Contains the main application code.
data/: Stores datasets and SQLite databases.
scripts/: Contains the precompute script for generating analytics data.
.env: Environment variables.
README.md: Setup and usage instructions.
requirements.txt: Python dependencies.
report.md: Implementation choices and challenges.
Report
For a detailed explanation of implementation choices and challenges faced, see the report.
