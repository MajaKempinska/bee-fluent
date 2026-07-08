from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# =========================================================
#  PRESENT SIMPLE
# =========================================================
QUESTIONS = [
    {
        "id": 1,
        "type": "sentence",
        "question": "Ułóż całe zdanie z wyrazów: always / I / coffee / drink / in the morning",
        "answer": "I always drink coffee in the morning",
        "explanation": "Picie kawy jest rutyną. Pamiętaj! Jeżeli mamy słówka dotyczące częstotliwości, tak jak tutaj „always”, to stoi ono przed czasownikiem — chyba że mamy „to be”, wtedy stoi po „am/are/is”.",
    },
    {
        "id": 2,
        "type": "sentence",
        "question": "Ułóż całe zdanie: she / never / late / is",
        "answer": "she is never late",
        "explanation": "To, że nigdy się nie spóźnia, jest faktem ogólnym z jej życia. Pamiętaj! Określenia dotyczące częstotliwości, np. „never”, stawiamy po czasowniku „to be” (am/are/is).",
    },
    {
        "id": 3,
        "type": "quiz",
        "question": "I ___ this song. (like)",
        "options": ["am liking", "like", "likes", "liking"],
        "answer": "like",
        "explanation": "„Like” to czasownik statyczny (wyraża uczucie), więc nigdy nie użyjemy go z końcówką „-ing”. Mówimy: I like this song (nie „I am liking”).",
    },
    {
        "id": 4,
        "type": "sentence",
        "question": "Ułóż całe zdanie: we / often / to the cinema / go",
        "answer": "we often go to the cinema",
        "explanation": "Chodzenie do kina jest rutyną. Pamiętaj! Jeżeli mamy słówka dotyczące częstotliwości, tak jak tutaj „often”, to stoi ono przed czasownikiem — chyba że mamy „to be”, wtedy stoi po „am/are/is”.",
    },
    {
        "id": 5,
        "type": "quiz",
        "question": "She ___ the answer. (know)",
        "options": ["is knowing", "knows", "know", "knowing"],
        "answer": "knows",
        "explanation": "„Know” to czasownik statyczny (wyraża stan wiedzy), więc nie występuje z „-ing”. „She” to 3. os. l. poj., więc dodajemy „-s”: She knows the answer.",
    },
    {
        "id": 6,
        "type": "sentence",
        "question": "Ułóż całe zdanie: he / rarely / television / watches",
        "answer": "he rarely watches television",
        "explanation": "To, że rzadko ogląda telewizję, jest rutyną. Pamiętaj! Jeżeli mamy słówka dotyczące częstotliwości, tak jak tutaj „rarely”, to stoi ono przed czasownikiem — chyba że mamy „to be”, wtedy stoi po „am/are/is”.",
    },
    {
        "id": 7,
        "type": "sentence",
        "question": "Ułóż zdanie: the plane / at 6 pm / leaves / London",
        "answer": "the plane leaves london at 6 pm",
        "explanation": "Mamy tu do czynienia z planem lotu, czyli elementem stałości. Często plany lotu są stałe przez kilka miesięcy/lat.",
    },
    {
        "id": 8,
        "type": "quiz",
        "question": "They ___ a big house. (have — posiadanie)",
        "options": ["are having", "have", "has", "having"],
        "answer": "have",
        "explanation": "W znaczeniu „posiadać” czasownik „have” jest statyczny i nie występuje z „-ing”. Dla „they” zostaje „have”: They have a big house. Uwaga! „Have” bywa też dynamiczne, gdy oznacza czynność — wtedy forma z „-ing” jest poprawna, np. „She is having breakfast” (je śniadanie) lub „I am having a shower”.",
    },
    {
        "id": 9,
        "type": "sentence",
        "question": "Ułóż zdanie: the meeting / on Monday / starts",
        "answer": "the meeting starts on monday",
        "explanation": "Mamy tu do czynienia z harmonogramem, czyli elementem stałości. Harmonogramy często są stałe przez kilka miesięcy/lat.",
    },
    {
        "id": 10,
        "type": "full",
        "question": "Zamień na przeczenie całym zdaniem: He plays football.",
        "answer": ["he doesn't play football", "he does not play football"],
        "explanation": "Pamiętaj! „Does” i „doesn't” zjada „-s”, dlatego: He plays football, ale He doesn't play football. Mowa tutaj o fakcie ogólnym z jego życia — „On nie gra w piłkę nożną”.",
    },
    {
        "id": 11,
        "type": "quiz",
        "question": "This soup ___ delicious. (taste)",
        "options": ["is tasting", "tastes", "taste", "tasting"],
        "answer": "tastes",
        "explanation": "Czasowniki opisujące wrażenia zmysłowe (np. taste — smakować, smell — pachnieć) są tu statyczne i nie łączą się z „-ing”. „This soup” to 3. os. l. poj., więc: This soup tastes delicious. Uwaga! „Taste” bywa też dynamiczne, gdy oznacza czynność próbowania — wtedy forma z „-ing” jest poprawna, np. „The chef is tasting the soup” (kucharz próbuje zupę).",
    },
    {
        "id": 12,
        "type": "full",
        "question": "Zamień na pytanie całym zdaniem: She drinks coffee.",
        "answer": "does she drink coffee",
        "explanation": "Pamiętaj! „Does” i „doesn't” zjada „-s”, dlatego: She drinks coffee, ale Does she drink coffee? Mamy tutaj pytanie dotyczące faktu ogólnego z jej życia — „Czy ona pije kawę?”.",
    },
    {
        "id": 13,
        "type": "sentence",
        "question": "Ułóż zdanie: the train / from platform 3 / departs",
        "answer": "the train departs from platform 3",
        "explanation": "Mamy tu do czynienia z rozkładem jazdy, czyli elementem stałości. Rozkłady jazdy często są stałe przez wiele miesięcy.",
    },
    {
        "id": 14,
        "type": "quiz",
        "question": "I ___ you are right. (think)",
        "options": ["am thinking", "think", "thinks", "thinking"],
        "answer": "think",
        "explanation": "W znaczeniu „sądzić, uważać” czasownik „think” jest statyczny i nie występuje z „-ing”: I think you are right. Uwaga! „Think” bywa też dynamiczne, gdy oznacza czynność zastanawiania się — wtedy forma z „-ing” jest poprawna, np. „I am thinking about my holidays” (myślę o wakacjach).",
    },
    {
        "id": 15,
        "type": "full",
        "question": "Zamień na przeczenie całym zdaniem: They like vegetables.",
        "answer": ["they don't like vegetables", "they do not like vegetables"],
        "explanation": "Dla I / you / we / they używamy „don't”. „Don't” nie zmienia formy czasownika: They like → They don't like. Mowa tutaj o fakcie ogólnym z ich życia — „Oni nie lubią warzyw”.",
    },
    {
        "id": 16,
        "type": "sentence",
        "question": "Ułóż zdanie: the flight / at 8 am / arrives / in Paris",
        "answer": "the flight arrives in paris at 8 am",
        "explanation": "Mamy tu do czynienia z planem lotu, czyli elementem stałości. Plany lotów są zaplanowane z góry i się nie zmieniają z dnia na dzień.",
    },
    {
        "id": 17,
        "type": "quiz",
        "question": "She ___ her sister very much. (love)",
        "options": ["is loving", "loves", "love", "loving"],
        "answer": "loves",
        "explanation": "„Love” to czasownik statyczny (uczucie), więc nie występuje z „-ing”. „She” to 3. os. l. poj., więc dodajemy „-s”: She loves her sister.",
    },
    {
        "id": 18,
        "type": "full",
        "question": "Zamień na pytanie całym zdaniem: You speak English.",
        "answer": "do you speak english",
        "explanation": "Dla I / you / we / they pytanie tworzymy przez „Do”: You speak English → Do you speak English? Mamy tutaj pytanie dotyczące faktu ogólnego — „Czy Ty mówisz po angielsku?”.",
    },
    {
        "id": 19,
        "type": "sentence",
        "question": "Ułóż zdanie: the course / in October / begins",
        "answer": "the course begins in october",
        "explanation": "Mamy tu do czynienia z harmonogramem, czyli elementem stałości. Harmonogramy zajęć są ustalone z góry na cały semestr.",
    },
    {
        "id": 20,
        "type": "quiz",
        "question": "She ___ every day. (swim)",
        "options": ["swim", "swims", "swimming", "swam"],
        "answer": "swims",
        "explanation": "Mowa tutaj o rutynie. W 3. os. l. poj. (he/she/it) dodajemy do czasownika „-s”: She swims. Pamiętaj! „Every day”, w przeciwieństwie do „always/often/sometimes”, wstawiamy na końcu zdania.",
    },
    {
        "id": 21,
        "type": "sentence",
        "question": "Ułóż zdanie: Christmas / on 25 December / falls",
        "answer": "christmas falls on 25 december",
        "explanation": "Mowa tutaj o święcie, czyli elemencie stałości. Święta wypadają w tym samym terminie co roku, dlatego używamy Present Simple.",
    },
    {
        "id": 22,
        "type": "quiz",
        "question": "The sun ___ in the east.",
        "options": ["rise", "rises", "rising", "rose"],
        "answer": "rises",
        "explanation": "To fakt ogólny (przyrodniczy). „The sun” to 3. os. l. poj., więc dodajemy „-s”: The sun rises.",
    },
    {
        "id": 23,
        "type": "sentence",
        "question": "Ułóż zdanie: Messi / the ball / passes / to Suarez",
        "answer": "messi passes the ball to suarez",
        "explanation": "To schematyczny komentarz sportowy — relacja na żywo, mimo że dzieje się teraz, opisywana jest w Present Simple. Komentarze sportowe są schematyczne, w pewnym sensie stałe — zmieniają się tylko nazwiska sportowców. Pamiętaj o „-s” w 3. os.: Messi passes.",
    },
    {
        "id": 24,
        "type": "quiz",
        "question": "They ___ like fruit. (przeczenie)",
        "options": ["doesn't", "don't", "isn't", "aren't"],
        "answer": "don't",
        "explanation": "Dla „they” w przeczeniu używamy „don't” (nie „doesn't”): They don't like fruit. Mowa tutaj o fakcie ogólnym z ich życia — „Oni nie lubią owoców”.",
    },
    {
        "id": 25,
        "type": "quiz",
        "question": "I ___ what you mean.",
        "options": ["am understanding", "understand", "understands", "understanding"],
        "answer": "understand",
        "explanation": "„Understand” to czasownik statyczny (stan umysłu), więc nie występuje z „-ing”. Mówimy: I understand what you mean.",
    },
    {
        "id": 26,
        "type": "sentence",
        "question": "Ułóż zdanie: the goalkeeper / the ball / catches",
        "answer": "the goalkeeper catches the ball",
        "explanation": "To komentarz sportowy — akcje na boisku relacjonujemy w Present Simple. Komentarze sportowe są schematyczne, w pewnym sensie stałe — zmieniają się tylko nazwiska sportowców. „The goalkeeper” to 3. os. l. poj., więc dodajemy „-s”: catches.",
    },
    {
        "id": 27,
        "type": "gap",
        "question": "Uzupełnij: He ___ (not / play) the piano. (2 słowa)",
        "answer": ["doesn't play", "does not play", "he doesn't play the piano", "he does not play the piano"],
        "explanation": "Pamiętaj! „Doesn't” zjada „-s”, dlatego: He doesn't play (a nie „doesn't plays”). Mowa tutaj o fakcie ogólnym z jego życia — „On nie gra na pianinie”.",
    },
    {
        "id": 28,
        "type": "sentence",
        "question": "Ułóż nagłówek: prices / rise / again",
        "answer": "prices rise again",
        "explanation": "To nagłówek artykułu. W nagłówkach prasowych używamy Present Simple, by brzmiały świeżo i dynamicznie. Nagłówki są poniekąd stałe, schematyczne — różnią się tylko miejsca oraz osoby (często gwiazdy lub politycy), których dotyczą. „Prices” to liczba mnoga, więc bez „-s”: rise.",
    },
    {
        "id": 29,
        "type": "quiz",
        "question": "This bag ___ to my mother. (belong)",
        "options": ["is belonging", "belongs", "belong", "belonging"],
        "answer": "belongs",
        "explanation": "„Belong” to czasownik statyczny (przynależność), więc nie występuje z „-ing”. „This bag” to 3. os. l. poj., więc dodajemy „-s”: This bag belongs to my mother.",
    },
    {
        "id": 30,
        "type": "sentence",
        "question": "Ułóż nagłówek: president / a new law / signs",
        "answer": "president signs a new law",
        "explanation": "To nagłówek artykułu. Nagłówki prasowe stosują Present Simple dla świeżości. Nagłówki są poniekąd stałe, schematyczne — różnią się tylko miejsca oraz osoby (często gwiazdy lub politycy), których dotyczą. „President” to 3. os. l. poj., więc dodajemy „-s”: signs.",
    },
    {
        "id": 31,
        "type": "gap",
        "question": "Uzupełnij: ___ he ___ tea? (drink — 2 słowa)",
        "answer": ["does drink", "does he drink tea"],
        "explanation": "Pamiętaj! „Does” zjada „-s”, dlatego w pytaniu: Does he drink tea? (a nie „drinks”). Pytanie o fakt ogólny z jego życia — „Czy on pije herbatę?”.",
    },
    {
        "id": 32,
        "type": "quiz",
        "question": "The museum ___ at 9 am. (open)",
        "options": ["open", "opens", "opening", "opened"],
        "answer": "opens",
        "explanation": "Mamy tu do czynienia z harmonogramem, czyli elementem stałości. Godziny otwarcia są stałe, a „the museum” to 3. os. l. poj., więc: The museum opens.",
    },
    {
        "id": 33,
        "type": "quiz",
        "question": "The ferry ___ every two hours. (leave)",
        "options": ["leave", "leaves", "leaving", "left"],
        "answer": "leaves",
        "explanation": "Mamy tu do czynienia z rozkładem jazdy, czyli elementem stałości. „The ferry” to 3. os. l. poj., więc dodajemy „-s”: The ferry leaves every two hours.",
    },
]

# =========================================================
#  PRESENT CONTINUOUS
# =========================================================
QUESTIONS_CONTINUOUS = [
    {
        "id": 1,
        "type": "quiz",
        "question": "Look! The baby ___ right now. (sleep)",
        "options": ["sleeps", "is sleeping", "sleep", "sleeping"],
        "answer": "is sleeping",
        "explanation": "„Right now” to sygnał Present Continuous — coś dzieje się w tym momencie. Budowa: is + czasownik z „-ing”: The baby is sleeping.",
    },
    {
        "id": 2,
        "type": "sentence",
        "question": "Ułóż zdanie: I / at the moment / English / am learning",
        "answer": "I am learning english at the moment",
        "explanation": "„At the moment” wskazuje na to, co dzieje się teraz. Budowa: am + czasownik z „-ing”: I am learning English at the moment.",
    },
    {
        "id": 3,
        "type": "quiz",
        "question": "She usually cooks, but today she ___ a pizza. (buy)",
        "options": ["buys", "is buying", "buy", "bought"],
        "answer": "is buying",
        "explanation": "To oderwanie od rutyny — zwykle gotuje (Present Simple), ale „today” wyjątkowo kupuje pizzę (Present Continuous): she is buying a pizza.",
    },
    {
        "id": 4,
        "type": "full",
        "question": "Zamień na pytanie całym zdaniem: You are reading a book.",
        "answer": "are you reading a book",
        "explanation": "W pytaniu „am/are/is” stawiamy przed osobą: You are reading → Are you reading a book? — „Czy czytasz książkę?”.",
    },
    {
        "id": 5,
        "type": "sentence",
        "question": "Ułóż zdanie: he / for his key / now / is looking",
        "answer": "he is looking for his key now",
        "explanation": "„Now” to sygnał teraźniejszości. Budowa: is + czasownik z „-ing”: He is looking for his key now — „On teraz szuka swojego klucza”.",
    },
    {
        "id": 6,
        "type": "quiz",
        "question": "I ___ to Spain tomorrow. (mam bilet, zaplanowane — fly)",
        "options": ["fly", "am flying", "flew", "will fly"],
        "answer": "am flying",
        "explanation": "Present Continuous wyraża też niedaleką, zaplanowaną przyszłość — mam bilet, więc to praktycznie na 100% pewne, że polecę: I am flying to Spain tomorrow.",
    },
    {
        "id": 7,
        "type": "quiz",
        "question": "Be careful — the weather ___ worse. (get)",
        "options": ["gets", "is getting", "get", "got"],
        "answer": "is getting",
        "explanation": "Present Continuous opisuje zachodzące zmiany. „The weather is getting worse” — pogoda się pogarsza.",
    },
    {
        "id": 8,
        "type": "sentence",
        "question": "Ułóż zdanie: it / cold / is getting",
        "answer": "it is getting cold",
        "explanation": "To zmiana, która właśnie zachodzi — używamy Present Continuous: It is getting cold — „Robi się zimno”.",
    },
    {
        "id": 9,
        "type": "quiz",
        "question": "Why are you always ___ so much noise? (irytacja: make)",
        "options": ["make", "making", "makes", "made"],
        "answer": "making",
        "explanation": "Present Continuous z „always” wyraża irytację powtarzającym się zachowaniem. Po „are you always” używamy czasownika z „-ing”: Why are you always making so much noise? — „Dlaczego zawsze tak hałasujesz?”.",
    },
    {
        "id": 10,
        "type": "full",
        "question": "Zamień na przeczenie całym zdaniem: She is watching TV.",
        "answer": ["she isn't watching tv", "she is not watching tv"],
        "explanation": "W przeczeniu dodajemy „not” po „am/are/is”: She is watching → She isn't watching TV — „Ona nie ogląda telewizji”.",
    },
    {
        "id": 11,
        "type": "quiz",
        "question": "This week she ___ London. (explore)",
        "options": ["explores", "is exploring", "explore", "explored"],
        "answer": "is exploring",
        "explanation": "„This week” podkreśla oderwanie od rutyny — wyjątkowo, w tym tygodniu, zwiedza Londyn: she is exploring London.",
    },
    {
        "id": 12,
        "type": "sentence",
        "question": "Ułóż zdanie: they / at the moment / are playing / football",
        "answer": "they are playing football at the moment",
        "explanation": "„At the moment” = teraz. Dla „they” używamy „are” + czasownik z „-ing”: They are playing football at the moment.",
    },
    {
        "id": 13,
        "type": "quiz",
        "question": "Listen! Someone ___ at the door. (knock)",
        "options": ["knocks", "is knocking", "knock", "knocked"],
        "answer": "is knocking",
        "explanation": "„Listen!” sygnalizuje, że coś dzieje się teraz. Budowa: is + czasownik z „-ing”: Someone is knocking at the door.",
    },
    {
        "id": 14,
        "type": "full",
        "question": "Zamień na pytanie całym zdaniem: They are having dinner.",
        "answer": "are they having dinner",
        "explanation": "„Am/are/is” przed osobą tworzy pytanie: They are having → Are they having dinner? Tu „have” jest dynamiczne (jeść kolację), więc forma z „-ing” jest poprawna.",
    },
    {
        "id": 15,
        "type": "sentence",
        "question": "Ułóż zdanie: I / not / am / working / this week",
        "answer": ["i am not working this week", "i'm not working this week"],
        "explanation": "Przeczenie: am + not + czasownik z „-ing”. To też oderwanie od rutyny: I am not working this week — „W tym tygodniu nie pracuję”.",
    },
]


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
    app.run(host="0.0.0.0", port=5001)