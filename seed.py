import os
import json
import psycopg2
from dotenv import load_dotenv
from app import QUESTIONS, QUESTIONS_CONTINUOUS

# Wczytaj connection string z .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Połącz się z bazą
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Stwórz tabelę (jeśli nie istnieje)
cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id            SERIAL PRIMARY KEY,
        tense         TEXT NOT NULL,
        original_id   INTEGER NOT NULL,
        type          TEXT NOT NULL,
        question      TEXT NOT NULL,
        answer        TEXT NOT NULL,
        options       TEXT,
        explanation   TEXT
    )
""")

# Wyczyść tabelę przed ponownym wgraniem (żeby nie dublować przy powtórnym uruchomieniu)
cur.execute("DELETE FROM questions")

def insert_questions(questions, tense):
    for q in questions:
        cur.execute(
            """INSERT INTO questions
               (tense, original_id, type, question, answer, options, explanation)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                tense,
                q["id"],
                q["type"],
                q["question"],
                json.dumps(q["answer"]),          # answer bywa listą -> JSON
                json.dumps(q.get("options")),     # options bywa listą -> JSON
                q.get("explanation", ""),
            )
        )

# Wgraj oba zestawy pytań
insert_questions(QUESTIONS, "present_simple")
insert_questions(QUESTIONS_CONTINUOUS, "present_continuous")

# Zapisz zmiany i zamknij
conn.commit()

cur.execute("SELECT COUNT(*) FROM questions")
count = cur.fetchone()[0]
print(f"Wgrano {count} pytań do bazy.")

cur.close()
conn.close()
