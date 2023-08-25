from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from pymongo import MongoClient
import bcrypt
from bson import ObjectId

app = Flask(__name__)
# Set the secret key for the Flask app
app.secret_key = "your_secret_key"

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view and unauthorized access message
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."

# Define the user_loader function
@login_manager.user_loader
def load_user(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(user_id)
    return None

client = MongoClient("mongodb+srv://your_connection_string")
db = client["Note_app"]
users = db["users"]
notes = db["notes"]

@app.route("/")
def index():
    if "user_id" in session:
        user_notes = notes.find({"user_id": session["user_id"]})
        return render_template("index.html", notes=user_notes)
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        users.insert_one({"username": username, "password": hashed_password})
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Retrieve user data from the 'users' collection
        user_data = db.users.find_one({"username": username})

        if user_data and bcrypt.checkpw(password.encode("utf-8"), user_data["password"]):
            session["user_id"] = str(user_data["_id"])
            return redirect(url_for("notes"))

    return render_template("login.html")

@app.route("/notes")
def notes():
    if "user_id" in session:
        user_notes = db.notes.find({"user_id": session["user_id"]})
        return render_template("index.html", notes=user_notes, current_user=current_user)
    return redirect(url_for("login"))

@app.route("/add_note", methods=["GET", "POST"])
def add_note():
    if "user_id" in session:
        if request.method == "POST":
            note_content = request.form["note_content"]
            task = request.form["task"]  # Get the task from the form
            time = request.form["time"]  # Get the time from the form
            db.notes.insert_one({
                "user_id": session["user_id"],
                "task": task,              # Insert the task field
                "content": note_content,
                "time": time               # Insert the time field
            })
            return redirect(url_for("notes"))
        return render_template("add_note.html")
    return redirect(url_for("login"))

@app.route("/edit_note/<note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    if "user_id" in session:
        note_collection = db["notes"]
        note = note_collection.find_one({"_id": ObjectId(note_id)})

        if note and note["user_id"] == session["user_id"]:
            if request.method == "POST":
                updated_task = request.form["task"]
                updated_content = request.form["updated_content"]
                updated_time = request.form["time"]

                note_collection.update_one(
                    {"_id": ObjectId(note_id)},
                    {
                        "$set": {
                            "task": updated_task,
                            "content": updated_content,
                            "time": updated_time
                        }
                    }
                )
                return redirect(url_for("notes"))

            return render_template("edit.html", note=note)

    return redirect(url_for("login"))

@app.route("/delete_note/<note_id>", methods=["POST", "DELETE"])
def delete_note(note_id):
    if "user_id" in session:
        note_collection = db["notes"]
        note = note_collection.find_one({"_id": ObjectId(note_id)})

        if note and note["user_id"] == session["user_id"]:
            note_collection.delete_one({"_id": ObjectId(note_id)})
            return redirect(url_for("notes"))
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
