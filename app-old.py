from flask import Flask, render_template, request, jsonify
from saisFunction.commands import process_user_input
from saisFunction.database import create_connection, delete_interactions_by_ids, insert_chat_interaction, get_all_chat_interactions, check_user_credentials, create_user
from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key


# Create a database connection
conn = create_connection()

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


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            user_id = 1  # Replace with the actual user ID
            response = process_user_input(user_id, user_input, conn)  # Pass user_id and the database connection
            return render_template("result.html", user_input=user_input, response=response)
    return render_template("home.html")

@app.route("/submit_command", methods=["POST"])
def submit_command():
    if request.method == "POST":
        user_input = request.form["user_input"]
        user_id = 1  # Replace with the actual user ID
        response = process_user_input(user_id, user_input, conn)  # Pass user_id and the database connection
        return render_template("result.html", user_input=user_input, response=response)

@app.route("/interactions", methods=["GET"])
def list_interactions():
    # Fetch chat interactions from the database
    interactions = get_all_chat_interactions(conn)
    #print(interactions[1])
    #print(interactions[1][0])
    #print(interactions[1][1])
    #print(interactions[1][2])
    #print(interactions[1][3])
    #print(interactions[1][4])
    return render_template("interactions.html", interactions=interactions)  # Pass 'interactions'

# ... REMOVE

@app.route("/remove_interactions", methods=["POST"])
def remove_interactions():
    if request.method == "POST":
        selected_ids = request.get_json().get("selected_ids")

        if selected_ids:
            # Remove the selected interactions from the database
            delete_interactions_by_ids(conn, selected_ids)

            return jsonify({"success": True, "message": "Interactions removed successfully"})
        else:
            return jsonify({"success": False, "message": "No interactions selected for removal"})

    return jsonify({"success": False, "message": "Invalid request"})



@app.route("/chat", methods=["GET"])
def chat():
    return render_template("chat.html")

# New route to handle saving messages in the database
@app.route("/save_message", methods=["POST"])
def save_message():
    if request.method == "POST":
        data = request.get_json()
        user_input = data.get("message")
        user_id = 1  # Replace with the actual user ID
        response = process_user_input(user_id, user_input, conn)  # Pass user_id and the database connection

        # Check if the message is not a duplicate and insert it into the database
        existing_chat_interactions = [interaction[2] for interaction in get_all_chat_interactions(conn)]
        if user_input not in existing_chat_interactions:
            insert_chat_interaction(conn, user_id, user_input, response)

        return jsonify({"success": True, "message": response})



    
if __name__ == '__main__':
    conn = create_connection()
    app.run(debug=True)    
