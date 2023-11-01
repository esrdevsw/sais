import unittest
from commands import greet_user, get_weather, search_wikipedia

class TestCommands(unittest.TestCase):
    def test_greet_user(self):
        self.assertEqual(greet_user(), "Hello! How can I assist you today?")

    def test_get_weather(self):
        # Modify this test with the expected weather response
        self.assertEqual(get_weather(), "The weather today is sunny with a high of 28°C.")

    def test_search_wikipedia(self):
        # Modify this test with the expected Wikipedia search response
        self.assertEqual(search_wikipedia(), "Wikipedia search result: [Your search result here]")

if __name__ == '__main__':
    unittest.main()
