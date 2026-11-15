# Kundenprojekt 02: Angebotsrechner für HansePack

**Verbindliches Briefing für Termine 6–8 · Version 1.0 · 08.11.2026**

## Der Kundenauftrag

HansePack Handelsgesellschaft ist ein fiktiver B2B-Händler für Verpackungsmaterial. Drei Vertriebsmitarbeitende erstellen Angebote bisher mit Tabellen und korrigieren Rabatt- und Versandfehler von Hand. Wir beauftragen eine kleine lokal ausführbare Webanwendung: Artikel und Mengen auswählen, Angebot berechnen, Ergebnis ansehen und als JSON herunterladen. Die Oberfläche darf deutsch oder englisch sein; Fachregeln und Pflichtumfang gelten für alle Teams identisch.

Die Anwendung ist ein eigenständiges Kundenprodukt in einem neuen Repo, beispielsweise `client-02-quotation`. Eure bestehende Factory entwickelt dieses Produkt. **Die Factory wird weiterverwendet; die Nordwerk-Website wird nicht zum Angebotsrechner umgebaut.** Ein bloß neuer Projektname bei hartcodierten Nordwerk-Pfaden ist keine Wiederverwendung.

## Lieferumfang und Technik

Eine einfache Seite mit Artikelauswahl, Menge, Positionen, Berechnung und Download genügt. Die Rechenlogik wird deterministisch in Python implementiert; FastAPI und einfaches HTML/CSS/JavaScript sind ohne zusätzliche Absprache zulässig. Bestehende Kursregeln für andere Frameworks bleiben bestehen. JSON-Katalog im Produkt reicht; keine Datenbank nötig. Der Produktbetrieb benötigt weder Factory noch LLM. Python-Version/Abhängigkeiten, Start- und Testaufruf werden dokumentiert. Kein Login, ERP, PDF, Zahlung, echte Kundendaten, öffentliche Bereitstellung oder KI im Produkt erforderlich.

## Artikelkatalog und verbindliche Fachregeln

Die Datei [HansePack_Katalog.json](HansePack_Katalog.json) ist verbindliche Eingabe, die folgenden Werte gelten pro Verkaufseinheit:

| SKU | Artikel | Preis in Cent | Anzeige in Euro |
|---|---|---:|---:|
| HP-BOX | Versandkarton / Shipping box | 250 | 2,50 |
| HP-TAPE | Klebeband / Packing tape | 400 | 4,00 |
| HP-FILM | Stretchfolie / Stretch film | 1250 | 12,50 |

1. Ein Angebot enthält 1–3 Positionen. Jede SKU darf höchstens einmal vorkommen. Mengen sind ganze Zahlen von 1 bis 10.000. Unbekannte Artikel, doppelte SKU, leere Liste, fehlende Werte, Strings statt Zahlen, Bruchmengen und boolesche Mengen sind ungültig. Keine stillschweigende Umwandlung, Rundung oder Zusammenfassung ungültiger Eingaben.
2. Pro Position: Listenbetrag = Menge × Einzelpreis. Der Mengenrabatt gilt für den **gesamten Listenbetrag dieser Position**, nicht stufenweise und nicht über mehrere Artikel summiert: 1–49 Einheiten 0 %, 50–99 Einheiten 5 %, ab 100 Einheiten 10 %.
3. Rabattbetrag pro Position auf ganze Cent **kaufmännisch aufrunden bei genau halbem Cent** (ROUND_HALF_UP). Positionsnetto = Listenbetrag − gerundeter Rabattbetrag. Ganzzahl-Cent oder Decimal verwenden; keine binäre Gleitkomma-Rundung. Bei ganzzahligen Prozentsätzen ist `(Listenbetrag_in_Cent * Rabattsatz + 50) // 100` eine mögliche Rabattberechnung.
4. Warenwert = Summe der Positionsnettobeträge. **Regelversion HP-V1, Termine 6/7:** Versand 1.200 Cent bei Warenwert unter 50.000 Cent, sonst 0 Cent. Schwelle einschließlich Gleichheit, nach Rabatt, vor Versand prüfen. Gesamt = Warenwert + Versand.
5. Ausschließlich simulierte Nettobeträge in EUR; keine Umsatzsteuerberechnung. Die Oberfläche kennzeichnet „Nettobeträge – Lehrprojekt, kein verbindliches Angebot“. Diese Übungsregel ist keine steuerrechtliche Empfehlung.
6. Ungültige Eingaben liefern verständliche Fehlermeldungen und kein scheinbar gültiges Angebot. Der genaue HTTP-Status ist nicht vorgeschrieben; Fehler und Erfolg müssen eindeutig unterscheidbar sein. Client-Prüfungen ersetzen keine Prüfung in der Python-Fachlogik.
7. Anzeige und JSON-Export enthalten SKU, Menge, Einzelpreis, Listenbetrag, Rabattsatz, Rabattbetrag und Nettobetrag je Position sowie Warenwert, Versand, Gesamt, Währung und Regelversion. Geldwerte im Export sind ganzzahlige Cent. Der Export stimmt exakt mit der sichtbaren Berechnung überein. Zeitstempel/Angebotsnummer sind optional und nicht Bestandteil der Referenzsummen.

## Referenzfälle – erwartete Ergebnisse

Diese Fälle sind vom Kunden vorgegeben, keine Ausgaben eures generierenden Agenten. Vollständige Eingaben und Positionswerte: [HansePack_Referenzfaelle.json](HansePack_Referenzfaelle.json). Tests dürfen die Daten laden; die Produktlogik darf nicht einfach erwartete Ergebnisse nach Fall-ID zurückgeben.

| Fall | Positionen | Warenwert Cent | Versand HP-V1 | Gesamt HP-V1 | Versand HP-V2 | Gesamt HP-V2 |
|---|---|---:|---:|---:|---:|---:|
| Q01 | BOX × 1 | 250 | 1200 | 1450 | 1500 | 1750 |
| Q02 | BOX × 49 | 12250 | 1200 | 13450 | 1500 | 13750 |
| Q03 | BOX × 50 | 11875 | 1200 | 13075 | 1500 | 13375 |
| Q04 | BOX × 99 | 23512 | 1200 | 24712 | 1500 | 25012 |
| Q05 | BOX × 100 | 22500 | 1200 | 23700 | 1500 | 24000 |
| Q06 | BOX × 200 | 45000 | 1200 | 46200 | 0 | 45000 |
| Q07 | FILM × 40 | 50000 | 0 | 50000 | 0 | 50000 |
| Q08 | FILM × 39 | 48750 | 1200 | 49950 | 0 | 48750 |
| Q09 | TAPE × 100 | 36000 | 1200 | 37200 | 1500 | 37500 |
| Q10 | FILM × 32 | 40000 | 1200 | 41200 | 0 | 40000 |
| Q11 | FILM × 31 | 38750 | 1200 | 39950 | 1500 | 40250 |
| Q12 | BOX × 50; TAPE × 10 | 15875 | 1200 | 17075 | 1500 | 17375 |
| Q13 | FILM × 51 | 60562 | 0 | 60562 | 0 | 60562 |
| Q14 | BOX × 53 | 12587 | 1200 | 13787 | 1500 | 14087 |

BOX/TAPE/FILM sind hier Kurzformen für die vollständigen SKU. Q04 rundet 1.237,5 Cent Rabatt auf 1.238 Cent; Q13 rundet 3.187,5 auf 3.188 Cent. Q06 prüft, dass die Versandschwelle nach dem Rabatt ausgewertet wird. Q14 verlangt 662,5 → 663 Cent Rabatt und unterscheidet HALF_UP vom Runden auf die nächste gerade Zahl.

## Abnahmekriterien: Was muss wann funktionieren?

Die Kennungen **HP-AC** bedeuten HansePack-Abnahmekriterien. Sie sind unabhängig von den Nordwerk-Kriterien AC-01–10.

| Kennung | Konkret gefordert | Fällig |
|---|---|---|
| HP-AC01 | Separates Produkt-Repo, dokumentierter unabhängiger Start und Testaufruf, keine Laufzeitabhängigkeit zur Factory. | T6 erster Stand; T7 frischer Checkout |
| HP-AC02 | Q01 und Q03 sind durch die Python-Fachlogik vollständig korrekt berechenbar; Ausgabe zeigt Positionen, Rabatt, Versand und Gesamt. | T6 |
| HP-AC03 | Alle Q01–Q14 unter HP-V1 einschließlich Positionswerten korrekt; Rabattgrenzen, Rundung und Versand stimmen. | T7 |
| HP-AC04 | Alle ungültigen Fälle E01–E10 der Referenzdatei werden in der Fachlogik zurückgewiesen; kein gültiges Angebot entsteht. | T7; T6 mindestens E01 |
| HP-AC05 | Einfache Weboberfläche: Positionen erfassen, berechnen, Ergebnis und verständliche Fehler anzeigen; Nettokennzeichnung sichtbar. | T7 |
| HP-AC06 | JSON-Export enthält die vorgeschriebenen Daten und stimmt mit Berechnung und Anzeige überein. | T7 |
| HP-AC07 | Frischer Checkout, reproduzierbare Produktprüfung, menschlicher Nutzungsreview und Release Candidate dokumentiert. | T7 |
| HP-AC08 | Änderung CR-02 erfüllt: alle Q01–Q14 mit HP-V2 korrekt, Rabatt-/Validierungsregeln erhalten, Anzeige und Export konsistent. | T8 |
| HP-AC09 | Versionierter Release, Übergabehinweise und wahrer technischer Freigabe-/Kundenabnahmestatus dokumentiert. | T8 |

## Bereits angekündigte Änderung CR-02 – erst Termin 8

„Wir passen unsere Versandbedingungen an: Unter 400,00 Euro Warenwert nach Rabatt berechnen wir 15,00 Euro Versand; ab einschließlich 400,00 Euro ist der Versand frei. Alles andere bleibt unverändert.“ Dies ist **HP-V2**. Keine rückwirkende Neuberechnung gespeicherter Angebote erforderlich, da Speicherung nicht Pflicht ist. V1 und V2 müssen nicht gleichzeitig im finalen Produkt auswählbar sein; historische V1-Stände bleiben über Git prüfbar. Tests müssen zur jeweiligen Regelversion passen, V2 darf nicht gegen alte V1-Versandwerte als fehlerhaft bewertet werden.

## Factory-Nachweis und Kosten

Je Termin mindestens ein echter Kunden-Task mit zwei zusammenarbeitenden Agentenfähigkeiten, strukturierten Übergaben, realem LLM über vorhandene Provider-Abstraktion, realer Tool-Nutzung und agentisch verändertem Produktcode oder anwendbarem Patch. Manuelle Anwendung/Korrektur erlaubt und erfasst. Externe Chat-/Editor-Nutzung allein ersetzt die eigene Factory nicht. Keine neuen Agentenquoten. Kursstack, lokale Modelle/HAW ICC, keine Cloud-Tokens.

Run-ID, Projektkennung, Task, tatsächlicher Factory-Commit, Produkt-Eingabe-/Ergebnis-Commit, Modell/Einstellungen, Tool-Aktionen, Tests, Reviewer, Entscheidung und Zeitpunkt verknüpfen. Saubere Ausgangsstände mit `git status` sichern. Manifest nach dem Produktstand in separatem Evidenz-Commit ablegen, keine zirkulären Hash-Anforderungen. Projektbereiche und Logs trennen; zweiter Kundenkontext darf nicht Nordwerk-Dateien überschreiben. Nordwerk-Produktstand als Commit sichern und nach Projektwechsel unverändert startbar halten; kein Neuaufbau des Altprojekts nötig.

Kurskostenmodell unverändert: Mensch 100 Credits/Personenstunde; Agentenaufruf 1 plus 0,01/s, Input 0,02/1.000 Tokens, Output 0,04/1.000 Tokens; CI-Workflow-Run 1 Credit, auch fehlgeschlagene Runs. Menschenzeit exklusiv als Factory-Entwicklung, Kundenlieferung, Review oder Nacharbeit zuordnen. Alle Fehlläufe zählen, unbekannte Werte `unknown`, bekannte Summen gegebenenfalls Teilkosten. Planbudget T6/T7 und Änderungsreserve T8 mit Dozent vereinbaren oder begründete Teamplanung verwenden; kein verborgenes Limit. Projektwechselaufwand separat markieren. Experimentlaufkosten und einmalige Verbesserungskosten getrennt ausweisen. Credits sind keine Euro-Prognose.

Abgabe je Termin: ein kurzer Index `evidence/session-06.md`, `session-07.md` bzw. `session-08.md` im Factory-Repo mit allen Verweisen und maximal drei nächsten Schritten. Zugängliche Repos oder überprüfbare ZIP-/Commit-/Diff-Nachweise bereitstellen; privater unzugänglicher Link genügt nicht. Technische Teamfreigabe und Dozenten-Kundenabnahme unterscheiden; ausstehende Kundenentscheidung kennzeichnen.
