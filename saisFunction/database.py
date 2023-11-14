import psycopg2

# Database connection parameters
DB_NAME = "saisdb"          # database name
DB_USER = "postgres"        # database username
DB_PASSWORD = "postgres"    # database password
DB_HOST = "localhost"       # database host
DB_PORT = "5432"            # database port (default is 5432)

# Establish a connection to the database
def create_connection():
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database - {e}")
        return None

# Create a table to store chat interactions
def create_chat_interactions_table(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_interactions (
                    id SERIAL PRIMARY KEY,
                    user_id INT,
                    user_message TEXT,
                    ai_response TEXT,
                    timestamp TIMESTAMP DEFAULT current_timestamp
                )
            """)
            conn.commit()
            cursor.close()
            print("Chat interactions table created successfully.")
        except psycopg2.Error as e:
            conn.rollback()  # Rollback the transaction in case of an error
            print(f"Error: Unable to create chat interactions table - {e}")
    else:
        print("Error: Database connection not established.")

# Insert a chat interaction into the database
def insert_chat_interaction(conn, user_id, user_message, ai_response):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chat_interactions (user_id, user_message, ai_response) VALUES (%s, %s, %s)", (user_id, user_message, ai_response))
            conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            conn.rollback()  # Rollback the transaction in case of an error
            print(f"Error: Unable to insert chat interaction - {e}")
    else:
        print("Error: Database connection not established.")

# Fetch all chat interactions from the database
def get_all_chat_interactions(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chat_interactions ORDER BY timestamp")
            chat_interactions = cursor.fetchall()
            cursor.close()
            return chat_interactions
        except psycopg2.Error as e:
            conn.rollback()  # Rollback the transaction in case of an error
            print(f"Error: Unable to fetch chat interactions - {e}")
            return []
    else:
        print("Error: Database connection not established.")
        return []



# Delete chat interactions by their IDs
def delete_interactions_by_ids(conn, interaction_ids):
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Create a comma-separated string of interaction IDs
            id_list = ', '.join(map(str, interaction_ids))
            # Execute the DELETE operation
            cursor.execute(f"DELETE FROM chat_interactions WHERE id IN ({id_list})")
            conn.commit()
            cursor.close()
            print("Chat interactions deleted successfully.")
        except psycopg2.Error as e:
            conn.rollback()  # Rollback the transaction in case of an error
            print(f"Error: Unable to delete chat interactions - {e}")
    else:
        print("Error: Database connection not established.")


# Check user credentials and return the user's role
def check_user_credentials(conn, username, password):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
            user_role = cursor.fetchone()
            cursor.close()
            return user_role[0] if user_role else None
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error: Unable to check user credentials - {e}")
    else:
        print("Error: Database connection not established.")

# Create a new user
def create_user(conn, username, password, role):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error: Unable to create user - {e}")
    else:
        print("Error: Database connection not established.")

def get_user_id_by_username(conn, username):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = cursor.fetchone()[0]  # Fetch the user_id
            cursor.close()
            return user_id
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error: Unable to fetch user_id - {e}")
            return None
    else:
        print("Error: Database connection not established.")
        return None


# Close the database connection
def close_connection(conn):
    if conn is not None:
        conn.close()
        print("Database connection closed.")
