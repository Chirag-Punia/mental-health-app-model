# Mental Health Chatbot

This is a Mental Health Chatbot built using FastAPI, Pinecone, and Google Gemini AI. It provides supportive responses to mental health-related queries by leveraging knowledge from books and web searches. The chatbot also performs emotion analysis and handles crisis situations responsibly.

## Features

- **Knowledge Base:** Answers queries using embeddings from provided books.
- **Emotion Analysis:** Detects user emotions from text input.
- **Crisis Handling:** Provides professional resources for crisis situations.
- **Web Search Fallback:** Performs web searches if no relevant data is found in the knowledge base.
- **FastAPI Backend:** Deployable as a REST API for frontend integration.

## Prerequisites

Before running the chatbot, ensure you have the following:

- **Python 3.9+**: Install from [python.org](https://www.python.org/).
- **API Keys:**
  - Pinecone API Key
  - Google Gemini API Key
  - SerpAPI Key
- **Books:** Provide PDF/EPUB files for the knowledge base (e.g., `medical_book.pdf`).

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mental-health-chatbot.git
cd mental-health-chatbot
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add your API keys:

```
PINECONE_API=your_pinecone_api_key
GEMINI_API=your_gemini_api_key
SERPAPI_API=your_serpapi_api_key
```

### 5. Process the Knowledge Base

Place your book files (e.g., `medical_book.pdf`) in the `data/` directory. Then, process the book to create embeddings:

```bash
python -m src.main --process-book data/medical_book.pdf
```

### 6. Run the Chatbot Locally

Start the FastAPI server:

```bash
uvicorn src.app:app --reload
```

The chatbot will be available at:

```
http://127.0.0.1:8000
```

## API Endpoints

### 1. Health Check

Check if the API is running:

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{"status": "healthy"}
```

### 2. Chat Endpoint

Send a query to the chatbot:

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"query": "I am feeling stressed"}'
```

Response:

```json
{
  "response": "It sounds like you're going through a tough time. Here are some tips to manage stress...",
  "emotion": {
    "emotion": "sadness",
    "confidence": 0.85
  }
}
```

## Deploy on Render (Optional)

To deploy the chatbot on Render and get a public API link, follow these steps:

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Create a `render.yaml` File

Add a `render.yaml` file to the root directory:

```yaml
services:
  - type: web
    name: mental-health-chatbot
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.app:app --host 0.0.0.0 --port 10000
    envVars:
      - key: PINECONE_API
        value: your_pinecone_api_key
      - key: GEMINI_API
        value: your_gemini_api_key
      - key: SERPAPI_API
        value: your_serpapi_api_key
```

### 3. Deploy on Render

- Go to [Render](https://render.com).
- Connect your GitHub repository.
- Render will automatically detect the `render.yaml` file and deploy your app.

## Troubleshooting

### 1. Out of Memory on Render

If the app runs out of memory on Render’s free tier:

- Use a smaller emotion analysis model (e.g., `bhadresh-savani/distilbert-base-uncased-emotion`).
- Remove unnecessary dependencies like TensorFlow.
- Upgrade to Render’s Starter Plan for more resources.

### 2. Missing API Keys

Ensure all API keys are correctly set in the `.env` file.

### 3. Import Errors

Use relative imports in your Python files (e.g., `from .config import Config`).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
