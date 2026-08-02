from flask import Flask, render_template, request
from database_config import user_collection
from routes.auth import auth
app = Flask(__name__)


app.register_blueprint(auth)

@app.route("/")
def index():
    return render_template("login.html")




if __name__ == "__main__":
    app.run(debug=True)