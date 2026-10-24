# CUST-001 – Clarifications / Klärungen

**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Projekt:** Kundenprojekt 01 – Website Release Candidate (Termin 3 Scope)  
**Erstellt durch:** Mehrose Farooq (Customer Lead / Product Owner)

| Question / Frage | Proposed assumption / Annahme | Customer answer / Kundenantwort | Date + confirmed by / bestätigt durch | Affected AC |
|---|---|---|---|---|
| Bisheriger PHP-Auftritt besaß ein CMS und Kontaktformular. Ist für den ersten Release Candidate eine statische Lösung ausreichend? | Ja, laut Briefing ist für den ersten neuen Auftritt eine rein statische HTML/CSS-Lösung mit E-Mail-Link (`mailto:`) akzeptiert. Kein CMS- oder PHP-Neubau erforderlich. | Bestätigt gemäß Kundenbriefing v1.0, 23.10.2026. | 2026-10-24, Mehrose Farooq (PO) | AC-01, AC-04, AC-08 |
| Sollen reale Test-E-Mails an `kontakt@nordwerk.example` gesendet werden? | Nein. `kontakt@nordwerk.example` ist ein RFC-2606-konformer Platzhalter. Es dürfen keine Nachrichten versendet werden. Der Link öffnet lediglich den lokalen Mail-Client. | Bestätigt gemäß Kundenbriefing v1.0. | 2026-10-24, Mehrose Farooq (PO) | AC-04 |
| Dürfen Kundenlogos, Zertifizierungen oder Erfolgsstatistiken ergänzt werden? | Nein. Laut Briefing sind keine erfundenen Kundenlogos, Zertifizierungen, Referenzen oder Erfolgszahlen zulässig. Ausschließlich autorisierte Texte (N-01 bis N-09). | Bestätigt gemäß Kundenbriefing v1.0. | 2026-10-24, Lars Boos (QA) | AC-01, AC-03 |
| Welcher Leistungsumfang ist für Termin 3 verbindlich fällig? | Für Termin 3 sind AC-01 (Firmenname & Hauptaussage), AC-04 (Kontaktlink & Übungshinweis) sowie eine erste Leistung aus AC-02 (N-03: Wartungsplanung) gefordert. Die weiteren Leistungen und Responsive-Tests folgen in T4. | Bestätigt gemäß Aufgabenblatt Termin 3. | 2026-10-24, Lars Boos (PM) | AC-01, AC-02, AC-04 |
