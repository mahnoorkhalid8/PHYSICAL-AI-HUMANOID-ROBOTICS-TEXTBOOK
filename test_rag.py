import requests
import json

# Test the RAG chatbot functionality
def test_rag_query():
    url = "http://localhost:8001/api/query"

    # Test query about the textbook content
    test_payload = {
        "question": "What is the Physical AI approach to humanoid robotics?",
        "selected_text": "",
        "context": {
            "search_scope": "full_book"
        }
    }

    print("Testing RAG query...")
    print(f"Sending request to: {url}")
    print(f"Payload: {json.dumps(test_payload, indent=2)}")

    try:
        response = requests.post(url, json=test_payload, timeout=30)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            response_data = response.json()
            print(f"Response Data: {json.dumps(response_data, indent=2)}")

            if "answer" in response_data:
                print("\n[SUCCESS] RAG query processed successfully!")
                print(f"Answer: {response_data['answer'][:200]}...")
            else:
                print("\n[ERROR] No answer in response")
                print(f"Full response: {response_data}")
        else:
            print(f"\n[ERROR] Request failed with status {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to the server. Make sure the backend is running on port 8001.")
    except requests.exceptions.Timeout:
        print("\n[ERROR] Request timed out. The query may be taking too long to process.")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")

if __name__ == "__main__":
    test_rag_query()