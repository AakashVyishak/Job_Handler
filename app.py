from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT,
                    company_name TEXT,
                    skills TEXT,
                    location TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_job():
    job_title = request.form["job_title"]
    company_name = request.form["company_name"]
    skills = request.form["skills"]
    location = request.form["location"]

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute("INSERT INTO jobs (job_title, company_name, skills, location) VALUES (?, ?, ?, ?)",
              (job_title, company_name, skills, location))
    conn.commit()
    conn.close()
    return ("", 204)

@app.route("/search_api")
def search_api():
    company = request.args.get("company", "")
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute("SELECT job_title, company_name, skills, location FROM jobs WHERE company_name LIKE ?", ('%'+company+'%',))
    results = c.fetchall()
    conn.close()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
