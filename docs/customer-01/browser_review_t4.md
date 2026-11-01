# Browser- & Bedienbarkeits-Review Termin 4 (AC-05, AC-06, AC-07 / Kriterien B3, B4)

**Kunde:** Nordwerk Industrie-Service (`client-01-website`)  
**Geprüfter Release-Candidate Commit / Tag:** `<CANDIDATE_COMMIT>` (Tag: `v0.2.0-rc1` / `R-BASE`)  
**Lokaler Startbefehl (ohne Factory):** `python -m http.server 8000 --directory client-01-website`  
**Geprüfte URL:** `http://localhost:8000`  
**Prüfer (benannter Mensch):** `David Pisarkiewicz` / `Lars Boos`  
**Datum:** 02. November 2026  

---

## 1. Responsive Prüfung an beiden Pflichtbreiten (AC-06 / Kriterium B3)

Geprüft über Chrome/Edge DevTools Device Toolbar (`Responsive`-Modus) sowie per Konsole (`document.documentElement.scrollWidth <= document.documentElement.clientWidth`):

| Viewport-Breite | Geprüfte Aspekte | Messwert `scrollWidth <= clientWidth` | Ergebnis | Prüfer |
|---|---|---|---|---|
| **375 px** (Mobil, z. B. iPhone SE / kleines Smartphone) | Kein horizontaler Scrollbalken/Überlauf; Navigation bricht sauber um (`flex-wrap: wrap`); Hero-Text, alle 3 Leistungskarten (`N-03`–`N-05`), Zielgruppen (`N-06`), Arbeitsweise (`N-07`) und Footer (`N-09`) vollständig lesbar; CTA-Button `Anfrage stellen` (`width: 100%` unter `600px`) gut antippbar. | `375 <= 375` (`true`) | **Bestanden** | David Pisarkiewicz / Lars Boos |
| **1280 px** (Desktop) | Zentrierter Inhaltsbereich (`max-width: 960px`), klare visuelle Hierarchie, kein Überlauf, alle Sektionen und Kontaktbuttons sofort nutzbar. | `1280 <= 1280` (`true`) | **Bestanden** | David Pisarkiewicz / Lars Boos |

---

## 2. Bedienbarkeit, Semantik & Tastaturfokus (AC-05, AC-07 / Kriterium B4)

| Prüfpunkt | Durchgeführte Prüfung im Browser & Markup | Ergebnis | Prüfer |
|---|---|---|---|
| **Dokumenttitel & Sprache (`AC-07`)** | `<html lang="de">` gesetzt; `<title>Nordwerk Industrie-Service ...</title>` im Browser-Tab sichtbar. | **Bestanden** | David Pisarkiewicz |
| **Überschriftenhierarchie (`AC-07`)** | Genau eine `<h1>` (`Nordwerk Industrie-Service`), gefolgt von `<h2>` je Sektion (`Leistungen`, `Zielgruppen`, `Arbeitsweise`, `Kontakt`) und `<h3>` je Leistungskarte (`Wartungsplanung`, `Ersatzteilkoordination`, `Betriebsdokumentation`). Keine Ebene übersprungen. | **Bestanden** | David Pisarkiewicz |
| **Tastaturnavigation & Fokus (`AC-07`)** | Durchtabben aller interaktiven Elemente mit der `Tab`-Taste (`Leistungen` $\rightarrow$ `Zielgruppen` $\rightarrow$ `Arbeitsweise` $\rightarrow$ `Kontakt` $\rightarrow$ Hero-CTA `Anfrage stellen` $\rightarrow$ Kontakt-CTA `Anfrage stellen`): Jedes fokussierte Element zeigt den deutlichen orangenen Fokusrahmen (`outline: 3px solid #d97706; outline-offset: 3px`). | **Bestanden** | Lars Boos |
| **Funktionierende Sprungmarken (`AC-05`)** | Klick bzw. `Enter` auf die Navigationslinks springt zum jeweiligen Abschnitt (`#leistungen`, `#zielgruppen`, `#arbeitsweise`, `#kontakt`) und hebt den Zielabschnitt visuell über `:target` hervor. | **Bestanden** | Lars Boos |
| **Kontaktlink (`AC-04`)** | Klick auf `Anfrage stellen` übergibt `mailto:kontakt@nordwerk.example` an das Betriebssystem (kein Seitenfehler, keine externe Weiterleitung). | **Bestanden** | Mehrose Farooq |
| **Bildalternativen (`AC-07`)** | Reine Text-/CSS-Seite ohne dekorative oder informative `<img>`-Elemente (automatisiert durch `test_website.py` Familie `F4` überwacht: 0 Bilder ohne `alt`). | **Bestanden (n/a)** | David Pisarkiewicz |
