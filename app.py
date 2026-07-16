from flask import Flask, request, jsonify, render_template
import re
import os
import json
import psycopg2
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics

load_dotenv()

app = Flask(__name__)
metrics = PrometheusMetrics(app)

DATABASE_URL = os.getenv("DATABASE_URL")


# =========================================================
#  WCZYTANIE PYTAŃ Z BAZY (raz przy starcie aplikacji)
# =========================================================
def load_questions_from_db():
    """Pobiera pytania z bazy i zwraca dwie listy: Present Simple i Present Continuous."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        "SELECT tense, original_id, type, question, answer, options, explanation "
        "FROM questions ORDER BY tense, original_id"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    simple = []
    continuous = []
    for tense, original_id, qtype, question, answer, options, explanation in rows:
        item = {
            "id": original_id,
            "type": qtype,
            "question": question,
            "answer": json.loads(answer),           # JSON -> string lub lista
            "explanation": explanation or "",
        }
        opts = json.loads(options) if options else None
        if opts is not None:
            item["options"] = opts

        if tense == "present_simple":
            simple.append(item)
        else:
            continuous.append(item)

    return simple, continuous


QUESTIONS, QUESTIONS_CONTINUOUS = load_questions_from_db()


# =========================================================
#  FUNKCJE POMOCNICZE
# =========================================================
def normalize(text):
    """Ujednolica tekst: małe litery, bez kropki i znaku zapytania na końcu, pojedyncze spacje."""
    text = text.strip().lower()
    text = text.rstrip(".?!")
    text = re.sub(r"\s+", " ", text)
    return text


def find_question(questions, qid):
    for q in questions:
        if q["id"] == qid:
            return q
    return None


def display_answer(question):
    """Zwraca odpowiedź do pokazania użytkownikowi (pierwszą, jeśli jest ich kilka)."""
    ans = question["answer"]
    if isinstance(ans, list):
        return ans[0]
    return ans


def build_safe_questions(questions):
    """Buduje listę pytań bez odpowiedzi (do wysłania na front)."""
    safe = []
    for q in questions:
        item = {"id": q["id"], "type": q["type"], "question": q["question"]}
        if q["type"] == "quiz":
            item["options"] = q["options"]
        safe.append(item)
    return safe


def check_answer(questions, data):
    """Wspólna logika sprawdzania odpowiedzi."""
    if not data or "id" not in data or "answer" not in data:
        return jsonify({"error": "Wymagane pola: id oraz answer"}), 400

    question = find_question(questions, data["id"])
    if not question:
        return jsonify({"error": "Nie ma pytania o takim id"}), 404

    user_answer = normalize(data["answer"])

    correct = question["answer"]
    if isinstance(correct, list):
        accepted = [normalize(a) for a in correct]
    else:
        accepted = [normalize(correct)]

    is_correct = user_answer in accepted

    return jsonify({
        "id": question["id"],
        "correct": is_correct,
        "correct_answer": display_answer(question),
        "explanation": question.get("explanation", ""),
    })


# =========================================================
#  TRASY
# =========================================================
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/present-simple")
def present_simple():
    return render_template("index.html")


@app.route("/present-continuous")
def present_continuous():
    return render_template("present-continuous.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# ----- Present Simple API -----
@app.route("/questions", methods=["GET"])
def get_questions():
    return jsonify(build_safe_questions(QUESTIONS))


@app.route("/check", methods=["POST"])
def check():
    return check_answer(QUESTIONS, request.get_json())


# ----- Present Continuous API -----
@app.route("/questions-continuous", methods=["GET"])
def get_questions_continuous():
    return jsonify(build_safe_questions(QUESTIONS_CONTINUOUS))


@app.route("/check-continuous", methods=["POST"])
def check_continuous():
    return check_answer(QUESTIONS_CONTINUOUS, request.get_json())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)