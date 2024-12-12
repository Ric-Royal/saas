# tests/test_ai_model.py

import unittest
from modules.ai_model import OllamaResponder

class TestOllamaResponder(unittest.TestCase):
    def test_generate_response_with_knowledge_graph(self):
        responder = OllamaResponder()
        prompt = "agriculture bill"
        print(f"Sending prompt: '{prompt}'")
        response = responder.generate_response(prompt)
        self.assertIsNotNone(response)
        self.assertNotEqual(response, "")
        print(f"AI Response: {response}")
        responder.close()

    def test_generate_response_without_knowledge_graph(self):
        responder = OllamaResponder()
        prompt = "unknown bill"
        print(f"Sending prompt: '{prompt}'")
        response = responder.generate_response(prompt)
        self.assertIsNotNone(response)
        self.assertNotEqual(response, "")
        print(f"AI Response: {response}")
        responder.close()

    def test_empty_prompt(self):
        responder = OllamaResponder()
        prompt = "   "
        print(f"Sending empty prompt.")
        response = responder.generate_response(prompt)
        self.assertEqual(response, "Please provide a valid query.")
        responder.close()

if __name__ == '__main__':
    unittest.main()
