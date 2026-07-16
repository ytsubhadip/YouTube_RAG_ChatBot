from flask import Flask
app = Flask(__name__)

@app.route("/status"):
    return 200;