import unittest
from database import create_connection, create_interaction_table, insert_interaction, get_all_interactions, close_connection

class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        # Create a temporary test database connection
        self.conn = create_connection()
        self.assertIsNotNone(self.conn, "Database connection not established")

    def test_create_interaction_table(self):
        # Test if the interaction table is created successfully
        create_interaction_table(self.conn)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM interactions")
        table_info = [desc[0] for desc in cursor.description]
        cursor.close()
        self.assertIn("id", table_info, "Table does not contain 'id' column")
        self.assertIn("user_input", table_info, "Table does not contain 'user_input' column")
        self.assertIn("response", table_info, "Table does not contain 'response' column")
        self.assertIn("created_at", table_info, "Table does not contain 'created_at' column")

    def test_insert_and_get_interactions(self):
        # Test inserting and fetching interactions
        create_interaction_table(self.conn)
        user_input = "Test input"
        response = "Test response"
        insert_interaction(self.conn, user_input, response)
        interactions = get_all_interactions(self.conn)
        self.assertEqual(len(interactions), 1, "Incorrect number of interactions")
        self.assertEqual(interactions[0][1], user_input, "User input doesn't match")
        self.assertEqual(interactions[0][2], response, "Response doesn't match")

    def tearDown(self):
        # Close the temporary test database connection
        close_connection(self.conn)

if __name__ == "__main__":
    unittest.main()
