# Termin 6 – Zweiter Kunde (HansePack) über eine zentrale Projekt-Registry

## Ziel
Die bestehende Factory unterstützt einen zweiten Kunden, HansePack (Angebotsrechner), ohne kopierte Agenten und ohne einen zweiten hartkodierten Agenten.
Projekt-spezifische Pfade, Repos und Default-Eingaben liegen zentral in einer Registry; ein Guard verhindert Schreibzugriffe in den Checkout des jeweils anderen Projekts.

## Projekt-Registry (`src/projects.py`)

| project_id | Kunde | Checkout-Ordner | Repo | Default-Input | Default-Test |
|---|---|---|---|---|---|
| `client-01` | Nordwerk Industrie-Service | `client-01-website` | `DavidPisark/Nordwerk-Industrie-Service-Website` | `index.html` | `test_website.py` |
| `client-02` | HansePack | `client-02-quotation` | `Vanitas50/client-02-quotation` | `quotation.py` | `test_quotation.py` |

Default-Issue für `client-02`: `issue_hp01.md` (wird genutzt, wenn `--issue-file` fehlt).

## Unverändert wiederverwendet
- Agenten unter `src/agents/`: `architect_agent.py`, `backend_agent.py`, `common.py`, `cost_agent.py`, `integration_agent.py`, `requirements_agent.py` (alle unverändert übernommen; `qa_security_agent.py` siehe unten).
- `organization/roles.yaml` und `organization/company.md` bleiben unverändert.
- `src/agents/common.py` (Pfad-Sicherheit: `REPO_ROOT`, `resolve_authorized_root`, `write_target_text_file`) bleibt unverändert und wird wiederverwendet.

## Angepasst (generisch, zentral)
- `src/projects.py` (neu): zentrale Registry als Python-Modul, keine neue Abhängigkeit (kein PyYAML).
- `src/workflows/feature_pipeline.py`: Default-Eingaben/Tests kommen bei gesetztem `--target-dir` aus der Registry; `assert_target_belongs_to_project` bricht vor jedem Schreiben ab, wenn ein fremder Checkout Ziel ist.
- `src/workflows/run_github_issue.py`: dieselben Defaults aus der Registry statt Nordwerk-fester Werte.
- `src/agents/qa_security_agent.py`: reine pytest-Dateien (mit `def test_`, ohne `__main__`) werden mit `pytest` statt `python datei.py` ausgeführt – verhindert falsches Grün.

## Bewusst nicht angepasst
- `src/quality/fault_injection.py` bleibt Nordwerk-spezifisch (Qualitätsnachweis aus Session 4). Für HansePack folgt eine eigene Fehlerinjektion erst bei Bedarf.

## Projekt-Trennung
Deterministischer Test `tests/test_project_separation_t6.py` (ohne Netz, ohne echtes LLM, in tmp-Verzeichnissen):
1. `test_hansepack_run_does_not_touch_nordwerk` – ein HansePack-Lauf ändert keine Nordwerk-Datei.
2. `test_client02_cannot_target_nordwerk_checkout` – client-02 darf den Nordwerk-Checkout nicht als Ziel wählen (ValueError).
3. `test_client01_cannot_target_hansepack_checkout` – spiegelbildlich für client-01.
4. `test_unknown_project_id_rejected` – unbekannte project_id wird abgelehnt.
5. `test_registry_defaults` – Registry-Defaults stimmen.

Aufruf: `python -m pytest tests/test_project_separation_t6.py`

## Gesicherter Nordwerk-Stand
Letzter Produkt-Commit `d140f26` auf `main` von `DavidPisark/Nordwerk-Industrie-Service-Website`; Release-Tag `CR-01-v1.0` = `f2feebb`.
HansePack-Arbeit findet ausschließlich in `client-02-quotation` statt.

## Aufruf für HansePack
```bash
python -m src.workflows.feature_pipeline --project-id client-02 --target-dir client-02-quotation --full-company --use-backend-agent --session session-06 --issue-file issue_hp01.md
```
Produkttest: `test_quotation.py` im Produkt-Repo (`python -m pytest -q`).
