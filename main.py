from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)

questions = [
    {
        "question": "Which is not in Europe?",
        "options": ["Paris", "Rome", "Argentina", "Berlin"],
        "answer": "Argentina"
    },
    {
        "question": "Which language is used for Android development?",
        "options": ["Java", "Python", "Ruby", "Swift"],
        "answer": "Java"
    }
]

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/play")
def play():
    q = random.choice(questions)
    options = q["options"][:]
    random.shuffle(options)
    return render_template("play.html", question=q["question"], options=options, correct=q["answer"])

@app.route("/submit", methods=["POST"])
def submit():
    selected = request.form.get("answer")
    correct = request.form.get("correct")
    return render_template("result.html", result="Correct!" if selected == correct else "Wrong!")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            q = request.form.get("question")
            options = [request.form.get(f"opt{i}") for i in range(1, 5)]
            correct = request.form.get("correct")
            questions.append({"question": q, "options": options, "answer": correct})
        elif action == "delete":
            index = int(request.form.get("index"))
            if 0 <= index < len(questions):
                questions.pop(index)
    return render_template("edit.html", questions=questions)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 81))
    app.run(host="0.0.0.0", port=port)
