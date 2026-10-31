# CUST-001 / TASK-001 – Clarifications / Klärungen & PHP-Sicherheitsanalyse

**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Projekt:** Kundenprojekt 01 – Website Release Candidate (Termin 3 Scope)  
**Erstellt durch:** Mehrose Farooq (Customer Lead / Product Owner) & David Pisarkiewicz (AI Safety & Security Engineer)

| Question / Frage | Proposed assumption / Annahme | Customer answer / Kundenantwort | Date + confirmed by / bestätigt durch | Affected AC |
|---|---|---|---|---|
| Bisheriger PHP-Auftritt besaß ein CMS und Kontaktformular. Ist für den ersten Release Candidate eine statische Lösung ausreichend? | Ja, laut Briefing ist für den ersten neuen Auftritt eine rein statische HTML/CSS-Lösung mit E-Mail-Link (`mailto:`) akzeptiert. Kein CMS- oder PHP-Neubau erforderlich. | Bestätigt gemäß Kundenbriefing v1.0, 23.10.2026. | 2026-10-26, Mehrose Farooq (PO) | AC-01, AC-04, AC-08 |
| Sollen reale Test-E-Mails an `kontakt@nordwerk.example` gesendet werden? | Nein. `kontakt@nordwerk.example` ist ein RFC-2606-konformer Platzhalter. Es dürfen keine Nachrichten versendet werden. Der Link öffnet lediglich den lokalen Mail-Client. | Bestätigt gemäß Kundenbriefing v1.0. | 2026-10-26, Mehrose Farooq (PO) | AC-04 |
| Dürfen Kundenlogos, Zertifizierungen oder Erfolgsstatistiken ergänzt werden? | Nein. Laut Briefing sind keine erfundenen Kundenlogos, Zertifizierungen, Referenzen oder Erfolgszahlen zulässig. Ausschließlich autorisierte Texte (`N-01` bis `N-09`). | Bestätigt gemäß Kundenbriefing v1.0. | 2026-10-26, Lars Boos (QA) | AC-01, AC-03 |
| Welcher Leistungsumfang ist für Termin 3 verbindlich fällig? | Für Termin 3 sind AC-01 (Firmenname & Hauptaussage), AC-04 (Kontaktlink & Übungshinweis) sowie eine erste Leistung aus AC-02 (`N-03`: Wartungsplanung) gefordert. Die weiteren Leistungen und Responsive-Tests folgen in T4. | Bestätigt gemäß Aufgabenblatt Termin 3. | 2026-10-26, Lars Boos (PM) | AC-01, AC-02, AC-04 |
| **LLM-Provider Google Gemini API (`gemini-3.8-flash`):** Dokumentarische Ausnahmegenehmigung statt rein lokalem Ollama/ICC | Zulässig über dokumentarischen Ausnahmeantrag ([`docs/GEMINI_PROVIDER_WAIVER.md`](../GEMINI_PROVIDER_WAIVER.md)): Exakte Einhaltung des Token-/Kostenmodells, Secrets-Isolation, 100 % Interoperabilität zu Ollama/ICC in `src/llm/factory.py` erhalten. | Ausnahmeantrag eingereicht und dokumentiert; Kosten und Tokens voll ausgewiesen. | 2026-10-31, Lars Boos (PM) & David Pisarkiewicz (Tech Lead) | A1, A2, C2 |
| **Aktuelle PHP-Sicherheitsvorfälle (`CVE-2026-109618` & `CVE-2026-109619`, ENISA-Warnung vom 21.10.2026):** Ist der bisherige PHP-8.2-Auftritt von Nordwerk betroffen und wie schützt der neue Release-Kandidat davor? | **Siehe detaillierte Sicherheitsbewertung unten:** Die pauschale Hoster-Angabe „PHP 8.2“ beweist weder Betroffenheit noch Sicherheit (Fix erst ab **PHP `8.2.35`**). Unser neuer Release-Kandidat (`client-01-website`) eliminiert jegliche PHP-Runtime-Angriffsfläche (`verify_no_php_attack_surface` in `test_website.py` & `detect_php_security_risks` in `qa_security_agent.py`). | Vorab-Sicherheitsberatung & technischer Guardrail in T3 umgesetzt; Vollbericht für SR-01 (AC-10) vorbereitet. | 2026-10-26, David Pisarkiewicz (Security) & Lars Boos (QA) | AC-04, AC-08, AC-10 (Vorbereitung SR-01) |

---

## Sicherheitsbewertung zu den kritischen PHP-Schwachstellen (ENISA Joint Statement vom 21.10.2026)

### 1. Technische Einordnung der aktuellen PHP-Vorfälle („PHP2Shell“)
Am **21. Oktober 2026** veröffentlichten die **ENISA** (European Union Agency for Cybersecurity), CERT-EU, EC3 und das EU CSIRTs Network ein dringendes Joint Statement zu zwei kritischen Remote-Code-Execution-(RCE)-Schwachstellen im PHP-Kern (Abrufdatum: 26.10.2026):
- **`CVE-2026-109618` (CVSS 9.2 – Out-of-Memory / `longjmp()` Memory Corruption):** Fehlerhafte Speicherbereinigung nach Überschreiten des `memory_limit` hinterlässt uninitialisierten Request-Speicher, was bei nachfolgenden Requests zu Speicherkorruption und unauthentifizierter Remote Code Execution (RCE) führt.
- **`CVE-2026-109619` (CVSS 9.2 – Global State Management Use-After-Free):** Globale PHP-Zustandszeiger referenzieren nach Request-Ende bereits freigegebenen Speicher und ermöglichen Angreifern über Folge-Requests beliebige Codeausführung (betrifft u. a. `PHP-FPM`, Apache `mod_php`, `php-cgi`, LiteSpeed, FrankenPHP).
- **Behobene PHP-Versionen laut PHP-Security-Release:** `8.5.12`, `8.4.27`, `8.3.36` sowie im 8.2-Zweig **`8.2.35`**.

### 2. Betroffenheit des bisherigen Nordwerk-Auftritts (Bestandsanalyse)
- **Was ist bekannt?** Der Alt-Auftritt läuft bei einem externen Hoster mit CMS und Kontaktformular unter der pauschalen Angabe „PHP 8.2“.
- **Was bleibt offen?** Die Angabe „PHP 8.2“ allein belegt **weder Betroffenheit noch Behebung**: Alle Versionen `< 8.2.35` sind verwundbar; erst `>= 8.2.35` ist gegen `CVE-2026-109618` und `CVE-2026-109619` gepatcht. Zudem ist unbekannt, ob das eingesetzte CMS eigene verwundbare PHP-Worker/Plugins mitbringt.
- **Was muss der externe Hoster sofort liefern?**
  1. Exakte PHP-Patchversion (`php -v` bzw. Paketstand des Betriebssystems, Nachweis `>= 8.2.35` oder Backport-Patch des Distributors).
  2. Verwendete Server-SAPI (`PHP-FPM`, `mod_php`, `php-cgi`) und Zeitpunkt des letzten Dienst-Neustarts nach dem Patch.
  3. CMS-Version und Prüfprotokoll auf bereits erfolgte Kompromittierung (Webshells / auffällige OOM-Einträge in den Error-Logs vor dem Patch).
- **Sofortmaßnahme für das Alt-System:** Solange der Hoster den Patchstand `>= 8.2.35` nicht schriftlich bestätigt, sollte der alte PHP-Auftritt (insbesondere das öffentlich erreichbare PHP-Kontaktformular) vorübergehend vom Netz genommen bzw. isoliert oder sofort durch unseren statischen Release-Kandidaten ersetzt werden.

### 3. Abgrenzung und technische Absicherung unseres neuen Release-Kandidaten (`client-01-website`)
- **Kein PHP-Laufzeitrisiko:** Unser neuer Webauftritt besteht ausschließlich aus statischem HTML5 (`index.html`) und CSS3 (`styles.css`) mit `mailto:`-Link und benötigt **keinerlei PHP-Interpreter oder Server-Skripte**.
- **Automatisierte Guardrails in Product & Factory:**
  - In `client-01-website/test_website.py` prüft `verify_no_php_attack_surface()`, dass im gesamten Produkt-Repo keine `.php`/`.phtml`/`.phar`/`.inc`/`.cgi`-Dateien, keine `<?php`/`<?=`-Tags und keine `.php`-Formular-Endpunkte existieren.
  - In `src/agents/qa_security_agent.py` prüft `detect_php_security_risks()` deterministisch auf PHP-RCE-Artefakte (abgesichert durch den Regressionstest `test_security_audit_flags_php_rce_surface_cve_2026_109618` in `tests/test_qa_security_agent.py`).
- **Ehrliche Abgrenzung („Statisch ≠ automatisch sicher“ & Funktionsverlust):**
  - Auch eine statische Website benötigt einen gepatchten ausliefernden HTTP-Server/Host und korrekte TLS-/Header-Konfiguration (Wartungsverantwortung beim Betreiber/Hoster).
  - Durch die Ablösung des PHP-CMS entfallen redaktionelle Online-Bearbeitung und das serverseitige Kontaktformular zugunsten des `mailto:`-Links (bewusster Trade-off zwischen Funktionsumfang und drastisch reduzierter Angriffsfläche).
