import psycopg2

# Database connection parameters
DB_NAME = "saisdb"          # Your database name
DB_USER = "postgres"   # Your database username
DB_PASSWORD = "postgres"  # Your database password
DB_HOST = "localhost"       # Your database host
DB_PORT = "5432"            # Your database port (default is 5432)

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

# Create a table to store interactions
def create_interaction_table(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id SERIAL PRIMARY KEY,
                    user_input TEXT,
                    response TEXT,
                    created_at TIMESTAMP DEFAULT current_timestamp
                )
            """)
            conn.commit()
            cursor.close()
            print("Interaction table created successfully.")
        except psycopg2.Error as e:
            print(f"Error: Unable to create interaction table - {e}")
    else:
        print("Error: Database connection not established.")

# Insert an interaction into the database
def insert_interaction(conn, user_input, response):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO interactions (user_input, response) VALUES (%s, %s)", (user_input, response))
            conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            print(f"Error: Unable to insert interaction - {e}")
    else:
        print("Error: Database connection not established.")

# Fetch all interactions from the database
def get_all_interactions(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM interactions ORDER BY created_at")
            interactions = cursor.fetchall()
            cursor.close()
            return interactions
        except psycopg2.Error as e:
            print(f"Error: Unable to fetch interactions - {e}")
            return []
    else:
        print("Error: Database connection not established.")
        return []
    

# Fetch all interactions from the database
def get_all_interactions(conn):
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM interactions ORDER BY created_at")
            interactions = cursor.fetchall()
            cursor.close()
            return interactions
        except psycopg2.Error as e:
            print(f"Error: Unable to fetch interactions - {e}")
            return []
    else:
        print("Error: Database connection not established.")
        return []

# Close the database connection
def close_connection(conn):
    if conn is not None:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    connection = create_connection()
    create_interaction_table(connection)
    close_connection(connection)
