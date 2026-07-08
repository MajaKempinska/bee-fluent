# 🐝 Bee Fluent — platforma do nauki gramatyki angielskiej

> © 2026 Maja Kempińska. Wszystkie prawa zastrzeżone.
> Kod udostępniony wyłącznie do wglądu w celach rekrutacyjnych i prezentacyjnych.

**🔗 Demo na żywo:** [bfwithmaja.azurewebsites.net](https://bfwithmaja.azurewebsites.net)

Interaktywna aplikacja webowa do nauki angielskich czasów gramatycznych,
z teorią i ćwiczeniami sprawdzanymi w czasie rzeczywistym. Zbudowana jako
realne narzędzie edukacyjne dla [Bee Fluent with Maja](https://bfwithmaja.com),
wdrożona w chmurze Azure z automatycznym pipeline CI/CD.

## ✨ Funkcje

- **Interaktywne lekcje** — Present Simple i Present Continuous
- **Trzy typy ćwiczeń** — wybór ABCD, uzupełnianie luk, układanie całych zdań
- **Sprawdzanie po stronie serwera** — poprawne odpowiedzi nie są widoczne w kodzie strony
- **Wyjaśnienia po każdej odpowiedzi** — nauka na błędach, nie tylko ocena
- **Elastyczne dopasowanie odpowiedzi** — akceptuje formy skrócone i pełne (np. `doesn't` / `does not`)

## 🛠️ Technologie

- **Backend:** Python, Flask, Gunicorn
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Konteneryzacja:** Docker
- **CI/CD:** GitHub Actions
- **Chmura:** Microsoft Azure (App Service)

## 🚀 Uruchomienie lokalne

```bash
git clone https://github.com/MajaKempinska/bee-fluent.git
cd bee-fluent

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Aplikacja będzie dostępna pod adresem `http://localhost:5001`.

### Uruchomienie w kontenerze Docker

```bash
docker build -t bee-fluent .
docker run -p 5001:5001 bee-fluent
```

## 🔄 CI/CD

Każdy push do gałęzi `main` automatycznie uruchamia pipeline GitHub Actions,
który buduje aplikację i wdraża ją na Azure App Service — bez ręcznych kroków.

## 📁 Struktura projektu
bee-fluent/
├── app.py                 # Backend Flask — logika i API ćwiczeń
├── requirements.txt       # Zależności
├── Dockerfile             # Definicja obrazu kontenera
├── templates/             # Szablony HTML
└── static/                # Obrazy i zasoby statyczne

## 🗺️ Plany rozwoju

- [x] Konteneryzacja (Docker)
- [x] CI/CD (GitHub Actions)
- [x] Wdrożenie w chmurze (Azure App Service)
- [ ] Testy automatyczne (pytest)
- [ ] Skan bezpieczeństwa w pipeline (Trivy)
- [ ] Infrastructure as Code (Terraform)
- [ ] Baza danych na pytania
- [ ] Kolejne czasy gramatyczne

## 📜 Prawa autorskie

© 2026 Maja Kempińska. Wszystkie prawa zastrzeżone.

Ten projekt — wraz z kodem źródłowym oraz treścią edukacyjną (teoria, ćwiczenia,
wyjaśnienia gramatyczne) — jest chroniony prawem autorskim i stanowi własność autorki.
Kopiowanie, modyfikowanie, rozpowszechnianie oraz wykorzystywanie kodu lub treści —
w całości lub w części — bez wyraźnej pisemnej zgody autorki jest zabronione.
