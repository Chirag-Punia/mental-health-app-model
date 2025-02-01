# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    PINECONE_API="pcsk_BUbYK_Pyudx3Gerwnm5nqrrfwisv4D5tbqnsxZnqrXWrE1zYBzohG8z2hDbjKJqsAZGzz" \
    GEMINI_API="AIzaSyCTyXXx0qZ6IzFNCJsU0W_DK3MJngsYudA" \
    SERPAPI_API="51bf1cded96c34b5bba5c63ac22961b36ebbad101281986be58406b940a8a893"

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port specified in the PORT environment variable
EXPOSE 8080

# Command to run the application
CMD exec uvicorn src.app:app --host 0.0.0.0 --port $PORT 

