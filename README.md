# 🐝 Bee Fluent — platforma do nauki gramatyki angielskiej

> © 2026 Maja Kempińska. Wszystkie prawa zastrzeżone.
> Kod udostępniony wyłącznie do wglądu w celach rekrutacyjnych i prezentacyjnych.

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
bee-fluent/
├── app.py                 # Backend Flask — logika i API ćwiczeń
├── requirements.txt       # Zależności
├── templates/             # Szablony HTML
│   ├── home.html          # Strona główna
│   ├── header.html        # Wspólny nagłówek
│   ├── index.html         # Lekcja Present Simple
│   └── present-continuous.html
└── static/                # Obrazy i zasoby statyczne

## 🗺️ Plany rozwoju

- [ ] Konteneryzacja (Docker)
- [ ] Testy automatyczne (pytest)
- [ ] CI/CD (GitHub Actions)
- [ ] Wdrożenie w chmurze
- [ ] Kolejne czasy gramatyczne

## 📜 Prawa autorskie

© 2026 Maja Kempińska. Wszystkie prawa zastrzeżone.

Ten projekt — wraz z kodem źródłowym oraz treścią edukacyjną (teoria, ćwiczenia,
wyjaśnienia gramatyczne) — jest chroniony prawem autorskim i stanowi własność autorki.

Kod został udostępniony publicznie **wyłącznie w celu prezentacji umiejętności**
(portfolio). Kopiowanie, modyfikowanie, rozpowszechnianie oraz wykorzystywanie
kodu lub treści — w całości lub w części, w celach komercyjnych lub niekomercyjnych —
bez wyraźnej pisemnej zgody autorki jest **zabronione**.

W sprawie ewentualnego wykorzystania proszę o kontakt: [bfwithmaja.com](https://bfwithmaja.com)
