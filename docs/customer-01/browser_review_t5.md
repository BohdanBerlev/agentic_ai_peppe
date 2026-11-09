# Manuelle Browser- und Tastaturprüfung – Termin 5 (`CR-01-v1.0`)

- **Projekt:** Kundenprojekt 01 – Nordwerk Industrie-Service (`client-01-website`)
- **Geprüfte Dateien:** `index.html` (Deutsche Ansicht) & `index_en.html` (Englische Einstiegsseite `CR-01`) + `styles.css`
- **Geprüfter Produkt-Commit:** `263d007` / `main` (Tag `CR-01-v1.0` / `v0.3.0`, erzeugt durch Factory-Lauf A `52b69365-3d49-4bcd-9c4d-f51ab8c136e7` und Factory-Lauf B `c0ee2cc3-4031-4ce9-8188-d37da99a1583`)
- **Prüfdatum:** `2026-11-09`
- **Prüfer (benannte Teammitglieder, D1 / B3):** Lars Boos & David Pisarkiewicz (Gegenprüfung: Mehrose Farooq)
- **Lokaler Startbefehl (ohne Factory):** `python -m http.server 8000 --directory client-01-website` (`http://localhost:8000/index.html` und `http://localhost:8000/index_en.html`)

---

## 1. Responsive Darstellungsprüfung bei `375 px` und `1280 px` (`AC-06`, `B1`–`B3`)

| Ansicht | Viewport | Geprüfte Aspekte | Messwert (`scrollWidth <= clientWidth`) | Ergebnis |
| :--- | :--- | :--- | :--- | :--- |
| **`index.html` (Deutsch)** | **`375 px`** (Mobil, `375 × 812`) | Kein horizontaler Überlauf (`overflow-x: hidden`), Navigation inklusive neuem Sprachlink `English` bricht sauber um (`flex-wrap: wrap`), neue Zielgruppe *„Technische Einkaufsabteilungen“* und alle Bausteine `N-01`–`N-09` vollständig lesbar. | `375 <= 375` (`true`) | **BESTANDEN** |
| **`index.html` (Deutsch)** | **`1280 px`** (Desktop, `1280 × 800`) | Zentrierter Container (`max-width: 960px`), klare visuelle Hierarchie, alle 3 Leistungskarten, 3 Zielgruppen, 3 Arbeitsweise-Punkte, Kontakt & Footer ohne Überlappung. | `1280 <= 1280` (`true`) | **BESTANDEN** |
| **`index_en.html` (Englisch `CR-01`)** | **`375 px`** (Mobil, `375 × 812`) | Kein horizontaler Überlauf, Header mit Navigation (`Services`, `Target Audiences`, `Contact`, `Deutsch`) bricht sauber um, alle 3 englischen Leistungskarten (*Maintenance planning*, *Spare parts coordination*, *Operational documentation*), Zielgruppe *Technical purchasing departments*, Button *Request information* (100 % Breite mobil) und Kurs-Hinweis im Footer klar lesbar. | `375 <= 375` (`true`) | **BESTANDEN** |
| **`index_en.html` (Englisch `CR-01`)** | **`1280 px`** (Desktop, `1280 × 800`) | Konsistentes Layout mit `styles.css`, klare Typografie, Sprachwechsel-Link `Deutsch` und Kontaktbutton `Request information` sofort erreichbar. | `1280 <= 1280` (`true`) | **BESTANDEN** |

---

## 2. Tastaturbedienbarkeit, Fokus-Sichtbarkeit & Sprachwechsel (`AC-05`, `AC-07`, `B2`, `B3`)

| Prüfschritt | Erwartetes Verhalten | Beobachtetes Verhalten im Browser | Ergebnis |
| :--- | :--- | :--- | :--- |
| **1. Tab-Reihenfolge auf `index.html` (DE)** | Alle interaktiven Links (`#leistungen`, `#zielgruppen`, `#arbeitsweise`, `#kontakt`, `index_en.html`, Hero-CTA `Anfrage stellen`, Kontakt-CTA `Anfrage stellen`) in logischer Reihenfolge per `Tab` erreichbar. | Exakt 7 Tab-Stopps in visueller Lesereihenfolge; jeder Link zeigt den orangenen Fokusrahmen (`outline: 3px solid #d97706; outline-offset: 3px`). | **BESTANDEN** |
| **2. Sprachwechsel DE $\rightarrow$ EN per Tastatur (`Enter`)** | Aktivieren von `<a href="index_en.html" hreflang="en" lang="en">English</a>` öffnet die englische Ansicht `index_en.html`. | Wechselt unmittelbar auf `/index_en.html` (`<html lang="en">`, Titel `Nordwerk Industrie-Service`). | **BESTANDEN** |
| **3. Tab-Reihenfolge auf `index_en.html` (EN)** | Alle interaktiven Links (`#leistungen`, `#zielgruppen`, `#kontakt`, `index.html`, CTA `Request information`) per `Tab` mit sichtbarem `:focus-visible`-Rahmen erreichbar. | Exakt 5 Tab-Stopps in logischer Reihenfolge; jeder Fokus-Zustand klar sichtbar; Sprungmarken `#leistungen`, `#zielgruppen`, `#kontakt` scrollen zum jeweiligen `<section id="...">`. | **BESTANDEN** |
| **4. Sprachwechsel EN $\rightarrow$ DE & Kontaktlink** | Aktivieren von `<a href="index.html" hreflang="de" lang="de">Deutsch</a>` führt zurück zur deutschen Startseite; Kontaktbuttons in beiden Ansichten verweisen auf `mailto:kontakt@nordwerk.example`. | Rückwechsel nach `index.html` sowie beide `mailto:kontakt@nordwerk.example`-Links (*Anfrage stellen* / *Request information*) funktionieren fehlerfrei. | **BESTANDEN** |

---

## 3. Gesamturteil der Browser- & Regressionsprüfung (Termin 5)

- **Technische Freigabe (Team 3):** **ERTEILT** durch Lars Boos, David Pisarkiewicz und Mehrose Farooq am `2026-11-09` (`0` Regressionen bei `AC-01`–`AC-08`, alle `CR-01`-Anforderungen erfüllt).
- **Kundenabnahme-Status:** **AUSSTEHEND** (wird im Rahmen von Termin 5 durch den Dozenten geprüft; keine Selbstbehauptung *„vom Kunden akzeptiert“*).
