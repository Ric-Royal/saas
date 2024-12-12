# tests/test_ollama_responder.py

from modules.ai_model import OllamaResponder

def main():
    try:
        responder = OllamaResponder()
        prompt = "Tell me about the Public Finance Management Amendment Bill 2024."
        response = responder.generate_response(prompt)
        print(f"AI Response: {response}")
        responder.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
