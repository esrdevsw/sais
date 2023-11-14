from flask import Flask, jsonify, render_template, request, redirect, send_from_directory, url_for, session
from saisFunction.commands import process_user_input
from saisFunction.database import create_connection, delete_interactions_by_ids, insert_chat_interaction, get_all_chat_interactions, check_user_credentials, create_user, get_user_id_by_username
import psycopg2


app = Flask(__name__, static_url_path='/static')

app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Create a database connection
conn = create_connection()


# # Function to check if the user is logged in
# @app.before_request
# def check_user_login():
#     if 'username' not in session and request.endpoint not in ['login', 'register']:
#         return redirect(url_for('login'))


# User login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_role = check_user_credentials(conn, username, password)
        if user_role:
            session['username'] = username
            session['role'] = user_role
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

# User registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'Normal User'  # Change as needed
        create_user(conn, username, password, role)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        # Clear the session data
        session.pop('username', None)
    return redirect(url_for('login'))



@app.route("/", methods=["GET", "POST"])
def home():
    if 'username' in session:
        username = session['username']
        user_id = get_user_id_by_username(conn, username)  # Fetch user_id based on the username
        if request.method == "POST":
            user_input = request.form.get("user_input")
            if user_input:
                response = process_user_input(user_id, user_input, conn)  # Use the obtained user_id
                return render_template("result.html", user_input=user_input, response=response)           
        
        return render_template("home.html")
    else:
        return redirect(url_for('login'))

@app.route("/submit_command", methods=["POST"])
def submit_command():
    if request.method == "POST":
        user_input = request.form["user_input"]
        username = session['username']
        user_id = get_user_id_by_username(conn, username)  # Fetch user_id based on the username
        response = process_user_input(user_id, user_input, conn)  # Use the obtained user_id
        return render_template("result.html", user_input=user_input, response=response)

@app.route("/interactions", methods=["GET"])
def list_interactions():
    interactions = get_all_chat_interactions(conn)
    return render_template("interactions.html", interactions=interactions)

@app.route("/remove_interactions", methods=["POST"])
def remove_interactions():
    if request.method == "POST":
        selected_ids = request.get_json().get("selected_ids")

        if selected_ids:
            delete_interactions_by_ids(conn, selected_ids)
            return jsonify({"success": True, "message": "Interactions removed successfully"})
        else:
            return jsonify({"success": False, "message": "No interactions selected for removal"})

    return jsonify({"success": False, "message": "Invalid request"})

@app.route("/chat", methods=["GET"])
def chat():
    return render_template("chat.html")

@app.route("/save_message", methods=["POST"])
def save_message():
    if request.method == "POST":
        data = request.get_json()
        user_input = data.get("message")
        username = session['username']
        user_id = get_user_id_by_username(conn, username)  # Fetch user_id based on the username
        response = process_user_input(user_id, user_input, conn)  # Use the obtained user_id

        existing_chat_interactions = [interaction[2] for interaction in get_all_chat_interactions(conn)]
        if user_input not in existing_chat_interactions:
            insert_chat_interaction(conn, user_id, user_input, response)

        return jsonify({"success": True, "message": response})

if __name__ == '__main__':
    conn = create_connection()
    app.run(debug=True)
