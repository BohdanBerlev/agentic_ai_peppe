# Fixture `nordwerk_rc`

Deterministische Test-Fixture für die Factory-Gate-Tests (`tests/test_quality_gate_t4.py`).

- `index.html` / `styles.css`: synthetische, vollständige Nordwerk-Seite (N-01–N-09), **nicht** das Kundenprodukt.
- `test_website.py` wird zur Testlaufzeit aus `client-01-website/test_website.py` kopiert, falls vorhanden;
  sonst wird die hier eingecheckte Snapshot-Kopie `product_check_snapshot.py` verwendet
  (Stand: Termin-4-Vorbereitung, Prüffamilien F1–F4).

Die Fixture belegt **deterministische Gate-Logik**, keinen realen LLM-Lauf.
