# Abnahme- & Übergabeprotokoll – Termin 5

**Produkt:** Nordwerk Industrie-Service Website  
**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-08  
**Session:** session-05

---

## 1. Technische Freigabe (Agent-Run-Ergebnis)

### CR-01: Englische Landing-Page + Zielgruppen-Erweiterung

| Prüfung | Ergebnis |
|---------|---------|
| `python test_website.py` (Regressionstest) | ✅ PASSED (F1–F4, 0 Fehler) |
| `python test_cr01.py` (CR-01-spezifisch) | ✅ PASSED (EN-01..DE-11) |
| Sprach-Switch DE→EN funktionsfähig | ✅ |
| "Technische Einkaufsabteilungen" in DE-View | ✅ |
| "Technical procurement departments" in EN-View | ✅ |

### Factory F-NEW-v1.0

| Prüfung | Ergebnis |
|---------|---------|
| `@lru_cache` auf `resolve_google_model()` | ✅ Implementiert |
| Verbessertes Logging | ✅ Implementiert |
| Modell unverändert (Gemini Flash) | ✅ Bestätigt |

---

## 2. Kunden-Entscheidung (CR-01)

**Status:** ⬜ Ausstehend – Kunde hat die englische Landing-Page noch nicht formal abgenommen.

**Offene Punkte:**
- Ist der Titel "Nordwerk Industrie-Service" (ohne Übersetzung) gewünscht?
- Sollen weitere Sprachen unterstützt werden?
- Soll die URL-Struktur (`index_en.html`) beibehalten werden oder wird eine Subdomain (`en.nordwerk.example`) bevorzugt?

---

## 3. Sicherheitsanfrage SR-01

**Status:** ✅ Beantwortet – siehe [`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md)

**Ergebnis:** Nordwerk-Website nicht betroffen (statisches HTML, kein PHP).  
**Ausstehend:** Hoster-Bestätigung (PHP deaktiviert).

---

## 4. Release-Tags

| Repo | Tag | Commit | Beschreibung |
|------|-----|--------|-------------|
| Factory | `F-NEW-v1.0` | `f803ece` | lru_cache + Logging |
| Produkt | `CR-01-v1.0` | `c4fbdba` | EN-Page + DE-Erweiterung |

---

## 5. Wartungsverantwortung

| Komponente | Verantwortlich | Intervall |
|-----------|---------------|---------|
| Gemini API-Key | Team / Betreiber | Bei Ablauf / Rotation |
| Website-Inhalte | Nordwerk / Team | Bei Änderungswunsch |
| Security-Checks | Team | Bei neuen CVE-Meldungen |
| PHP-Status beim Hoster | Nordwerk | Bei Hosting-Wechsel |

---

*Erstellt von PepeGroup (Team 3) als Abnahmedokument für Session 5.*
