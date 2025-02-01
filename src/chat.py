import requests

# API endpoint
API_URL = "http://127.0.0.1:8000/chat"

def start_chat():
    print("Welcome to the Mental Health Chatbot! Type 'exit' to end the chat.")
    session_id = None  # Initialize session ID

    while True:
        # Get user input
        query = input("You: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break

        # Prepare the request payload
        payload = {"query": query}
        if session_id:
            payload["session_id"] = session_id

        # Send the request to the chatbot API
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"Assistant: {data['response']}")
            session_id = data["session_id"]  # Update session ID
        else:
            print("Error: Unable to get a response from the chatbot.")

if __name__ == "__main__":
    start_chat()