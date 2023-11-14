from database import create_connection, create_chat_interactions_table

# Create a connection to the database
conn = create_connection()

# Check if the connection is established
if conn:
    # Create the chat_interactions table
    create_chat_interactions_table(conn)
    conn.close()  # Close the connection

print("Chat interactions table created successfully.")
