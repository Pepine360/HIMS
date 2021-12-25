from api import app
from flask import render_template, url_for


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="192.168.2.25", port='8000')
