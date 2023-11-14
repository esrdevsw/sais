import psycopg2

# Database connection parameters
DB_NAME = "saisdb"          # database name
DB_USER = "postgres"        # database username
DB_PASSWORD = "postgres"    # database password
DB_HOST = "localhost"       # database host
DB_PORT = "5432"            # database port (default is 5432)

# Establish a connection to the database
conn = psycopg2.connect(
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Create a cursor
cursor = conn.cursor()

# Function to create a user with a specified role
def create_user_with_role(username, password, role):
    try:
        # Execute the INSERT query to create a new user
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        conn.commit()
        print(f"User '{username}' with role '{role}' created successfully.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error: Unable to create user - {e}")

# Create an administrator user
create_user_with_role("admin", "admin_password", "Admin")

# Close the cursor and database connection
cursor.close()
conn.close()

