from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("./scripts/", "index.js")

@app.route("/roll")
def roll():
    return send_from_directory("./static/", "video copy.html")

if __name__ == "__main__":
    app.run(debug=True)