from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Load users from JSON
USERS_PATH = os.path.join("data", "users.json")
with open(USERS_PATH, "r") as f:
    users = json.load(f)

# Sample quiz questions (10 for demo)
QUESTIONS = [
    {"id": 1, "text": "Learning a new programming language:"},
    {"id": 2, "text": "Understanding how an Operating System manages processes:"},
    {"id": 3, "text": "When learning about Computer Networks:"},
    {"id": 4, "text": "To prepare for a Data Structures exam:"},
    {"id": 5, "text": "While understanding Database Management Systems (DBMS):"},
    {"id": 6, "text": "If asked to learn about Software Development Life Cycle (SDLC):"},
    {"id": 7, "text": "When debugging an error in code:"},
    {"id": 8, "text": "To revise before a semester exam:"},
    {"id": 9, "text": "When learning about Computer Architecture:"},
    {"id": 10, "text": "While learning about Machine Learning algorithms:"}
]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid credentials!")
    return render_template("login.html")

@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", name=session["username"])

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        scores = {"Visual": 0, "Auditory": 0, "Reading": 0, "Kinesthetic": 0}

        for q in QUESTIONS:
            ans = request.form.get(f"q{q['id']}")
            if ans == "V": scores["Visual"] += 1
            elif ans == "A": scores["Auditory"] += 1
            elif ans == "R": scores["Reading"] += 1
            elif ans == "K": scores["Kinesthetic"] += 1

        max_score = max(scores.values())
        dominant = [k for k, v in scores.items() if v == max_score]
        learner_type = "Unimodal" if len(dominant) == 1 else "Multimodal"
        dominant_str = ", ".join(dominant)

        if "Kinesthetic" in dominant:
            recommended = "Practical-Oriented Courses"
        elif "Visual" in dominant or "Reading" in dominant:
            recommended = "Theory-Oriented Courses"
        else:
            recommended = "Balanced (Theory + Practical) Courses"

        return render_template(
            "result.html",
            name=session["username"],
            learner_type=learner_type,
            dominant=dominant_str,
            recommended=recommended,
            scores=scores
        )

    return render_template("quiz.html", questions=QUESTIONS)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
