from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    with sqlite3.connect("bot.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM resumes ORDER BY timestamp DESC LIMIT 50")
        resumes = cur.fetchall()
    return render_template("index.html", resumes=resumes)

if __name__ == "__main__":
    app.run(debug=True)