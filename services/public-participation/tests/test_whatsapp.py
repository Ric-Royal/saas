# tests/test_whatsapp_bot.py

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from scripts.whatsapp_bot import app, responder, knowledge_graph

class TestWhatsAppBot(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('whatsapp_bot.search_bills')
    @patch('whatsapp_bot.responder.generate_response')
    def test_response_with_knowledge_graph_data(self, mock_generate_response, mock_search_bills):
        # Mock the Knowledge Graph to return data
        mock_search_bills.return_value = ["Bill Title: Agriculture Act\nSection 1: Conservation Programs", 
                                         "Bill Title: Agriculture Act\nSection 2: Trade Agreements"]

        # Mock the AI response
        mock_generate_response.return_value = "The Agriculture Act focuses on conservation and trade agreements..."

        response = self.app.post('/whatsapp', data={
            'Body': 'agriculture bill',
            'From': '+1234567890'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The Agriculture Act focuses on conservation and trade agreements...", response.data)

    @patch('whatsapp_bot.search_bills')
    @patch('whatsapp_bot.responder.generate_response')
    def test_response_without_knowledge_graph_data(self, mock_generate_response, mock_search_bills):
        # Mock the Knowledge Graph to return no data
        mock_search_bills.return_value = []

        # Mock the AI response
        mock_generate_response.return_value = "I'm sorry, I couldn't find any specific bills related to that. Could you please provide more details?"

        response = self.app.post('/whatsapp', data={
            'Body': 'unknown bill',
            'From': '+1234567890'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"I'm sorry, I couldn't find any specific bills related to that. Could you please provide more details?", response.data)

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"OK", response.data)

    def test_empty_message(self):
        response = self.app.post('/whatsapp', data={
            'Body': '   ',
            'From': '+1234567890'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello! How can I assist you with Kenyan bills today?", response.data)

    @patch('whatsapp_bot.responder.generate_response', side_effect=Exception("AI Error"))
    def test_ai_error_handling(self, mock_generate_response):
        # Mock the Knowledge Graph to return data
        with patch('whatsapp_bot.search_bills', return_value=["Bill Title: Agriculture Act\nSection 1: Conservation Programs"]):
            response = self.app.post('/whatsapp', data={
                'Body': 'agriculture bill',
                'From': '+1234567890'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Sorry, an error occurred while processing your request.", response.data)

if __name__ == '__main__':
    unittest.main()
