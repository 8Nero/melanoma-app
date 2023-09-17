from flask import Flask
from flask_ngrok2 import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/")
def home():
    return "<h1>Welcome!</h1>"

if(__name__ == '__main__'):
    app.run()