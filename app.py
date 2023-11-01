from flask import Flask, render_template, request
from saisFunction.commands import process_user_input
from saisFunction.database import create_connection, get_all_interactions
import atexit  # Import atexit module to handle cleanup

app = Flask(__name__)

# Create a database connection
conn = create_connection()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            response = process_user_input(user_input, conn)  # Pass the database connection
            return render_template("result.html", user_input=user_input, response=response)
    return render_template("home.html")

@app.route("/submit_command", methods=["POST"])
def submit_command():
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = process_user_input(user_input, conn)  # Pass the database connection
        return render_template("result.html", user_input=user_input, response=response)

@app.route("/interactions", methods=["GET"])
def list_interactions():
    # Fetch interactions from the database
    interactions = get_all_interactions(conn)
    return render_template("interactions.html", interactions=interactions)

# Register a function to close the database connection when the application is done
def close_db_connection():
    if conn is not None:
        conn.close()
        print("Database connection closed.")

atexit.register(close_db_connection)

if __name__ == "__main__":
    app.run(debug=True)
