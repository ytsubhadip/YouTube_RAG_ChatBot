import os
from flask import Flask, render_template, request, session
from database_config import user_collection
from routes.auth import auth
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = "my_secret_key_123"

app.register_blueprint(auth)

@app.route("/")
def index():

    return render_template("login.html")

@app.route("/chatbox")
def chatbox():
    if "user" in session:
        return render_template("chatbox.html")
    else:
        return {"message": "page not found"}

    




if __name__ == "__main__":
    app.run(debug=True)