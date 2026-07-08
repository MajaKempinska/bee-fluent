# 🐝 Bee Fluent — platforma do nauki gramatyki angielskiej

Interaktywna aplikacja webowa do nauki angielskich czasów gramatycznych,
z teorią i ćwiczeniami sprawdzanymi w czasie rzeczywistym. Zbudowana jako
realne narzędzie edukacyjne dla [Bee Fluent with Maja](https://bfwithmaja.com).

## ✨ Funkcje

- **Interaktywne lekcje** — Present Simple i Present Continuous
- **Trzy typy ćwiczeń** — wybór ABCD, uzupełnianie luk, układanie całych zdań
- **Sprawdzanie po stronie serwera** — poprawne odpowiedzi nie są widoczne w kodzie strony
- **Wyjaśnienia po każdej odpowiedzi** — nauka na błędach, nie tylko ocena
- **Elastyczne dopasowanie odpowiedzi** — akceptuje formy skrócone i pełne (np. `doesn't` / `does not`)

## 🛠️ Technologie

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Serwer produkcyjny:** Gunicorn

## 🚀 Uruchomienie lokalne

```bash
# Sklonuj repozytorium
git clone https://github.com/MajaKempinska/bee-fluent.git
cd bee-fluent

# Utwórz i aktywuj środowisko wirtualne
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom aplikację
python app.py
```

Aplikacja będzie dostępna pod adresem `http://localhost:5001`.

## 📁 Struktura projektu
