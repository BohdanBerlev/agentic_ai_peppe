"""
Automated product verification for Nordwerk Industrie-Service (Release Candidate, Termin 4).

Prueffamilien (Aufgabenblatt Termin 4, Abschnitt 3 / Bewertungskriterium B6):
  F1 Pflichtinhalt          - N-01 bis N-09 aus dem Kundenbriefing, keine erfundenen Versprechen (AC-01, AC-02, AC-03, AC-04)
  F2 Kontakt & Navigation   - mailto:kontakt@nordwerk.example mit "Anfrage stellen", Navigation zu Leistungen
                              und Kontakt, jedes interne #-Ziel existiert (AC-04, AC-05)
  F3 Lokale Verweise/Assets - alle lokalen href/src existieren im Checkout, keine externen Abhaengigkeiten,
                              keine PHP-Angriffsflaeche (AC-05, AC-08; CVE-2026-109618 / CVE-2026-109619)
  F4 Bedienbarkeit (statisch) - Titel, lang="de", genau eine h1, keine uebersprungenen Ueberschriftenebenen,
                              Alt-Texte, Viewport-Meta, sichtbarer Tastaturfokus (AC-06/AC-07 statischer Anteil;
                              375/1280 px und Tab-Navigation werden zusaetzlich im Browser geprueft)

Start ohne Factory:  python test_website.py      (Exit-Code 0 = bestanden)
oder:                python -m pytest -q test_website.py
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

CONTACT_MAILTO = "mailto:kontakt@nordwerk.example"
CONTACT_LABEL = "Anfrage stellen"
SERVICES_ANCHOR = "leistungen"
CONTACT_ANCHOR = "kontakt"

# Pflichtinhalte gemaess Kundenbriefing v1.0 (Layout/Ueberschriften duerfen ergaenzt werden).
REQUIRED_CONTENT: dict[str, str] = {
    "N-01 Firmenname": "Nordwerk Industrie-Service",
    "N-02 Hauptaussage": "Praktische Unterstützung für Ihren technischen Betrieb.",
    "N-03 Leistung Wartungsplanung (Titel)": "Wartungsplanung",
    "N-03 Leistung Wartungsplanung (Text)": (
        "Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe."
    ),
    "N-04 Leistung Ersatzteilkoordination (Titel)": "Ersatzteilkoordination",
    "N-04 Leistung Ersatzteilkoordination (Text)": (
        "Wir unterstützen bei der Abstimmung von Ersatzteilbedarfen und Lieferterminen."
    ),
    "N-05 Leistung Betriebsdokumentation (Titel)": "Betriebsdokumentation",
    "N-05 Leistung Betriebsdokumentation (Text)": (
        "Wir bringen technische Unterlagen in eine nachvollziehbare und nutzbare Struktur."
    ),
    "N-06 Zielgruppe 1": "Kleine Produktionsbetriebe",
    "N-06 Zielgruppe 2": "Technische Serviceunternehmen",
    "N-07 Arbeitsweise": (
        "Ein fester Ansprechpartner, ein gemeinsam vereinbarter Leistungsumfang und nachvollziehbare Ergebnisse."
    ),
    "N-08 Kontakt-Beschriftung": CONTACT_LABEL,
    "N-09 Uebungshinweis": (
        "Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme."
    ),
}

# Erfundene Leistungsversprechen / Tracker, die das Briefing ausdruecklich ausschliesst.
FORBIDDEN_CLAIMS = [
    "ISO 9001",
    "TÜV",
    "zertifiziert",
    "24/7",
    "Notdienst",
    "Garantie",
    "Reaktionszeit",
    "Referenzkunden",
    "google-analytics",
    "gtag(",
]

FORBIDDEN_SERVER_MARKERS = ["<?php", "<?="]
FORBIDDEN_PHP_EXTENSIONS = {".php", ".phtml", ".phar", ".php5", ".php7", ".php8", ".inc", ".cgi"}
IGNORED_DIRS = {".git", "__pycache__", ".idea", ".pytest_cache", "node_modules"}


class _PageParser(HTMLParser):
    """Collect visible text, links, ids, headings, images and asset references."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text_parts: list[str] = []
        self.ids: set[str] = set()
        self.anchors: list[dict] = []  # {"href", "text", "in_nav"}
        self.assets: list[tuple[str, str]] = []  # (tag, url)
        self.headings: list[int] = []
        self.images_without_alt: list[str] = []
        self.title = ""
        self.html_lang = ""
        self.has_viewport = False
        self._in_title = False
        self._nav_depth = 0
        self._skip_depth = 0
        self._open_anchor: dict | None = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "html":
            self.html_lang = a.get("lang", "")
        elif tag == "title":
            self._in_title = True
        elif tag in ("script", "style"):
            self._skip_depth += 1
        elif tag == "nav":
            self._nav_depth += 1
        elif tag == "meta" and a.get("name", "").lower() == "viewport":
            self.has_viewport = True
        elif re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))
        elif tag == "img":
            if "alt" not in a:
                self.images_without_alt.append(a.get("src", "?"))
        if tag == "a" and "href" in a:
            self._open_anchor = {"href": a["href"].strip(), "text": "", "in_nav": self._nav_depth > 0}
            self.anchors.append(self._open_anchor)
        for attr in ("href", "src"):
            if attr in a and tag != "a":
                self.assets.append((tag, a[attr].strip()))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1
        elif tag == "nav" and self._nav_depth:
            self._nav_depth -= 1
        elif tag == "a":
            self._open_anchor = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._skip_depth:
            return
        self.text_parts.append(data)
        if self._open_anchor is not None:
            self._open_anchor["text"] += data

    @property
    def visible_text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.text_parts)).strip()


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _load(root: Path) -> tuple[str, _PageParser]:
    html = (root / "index.html").read_text(encoding="utf-8")
    parser = _PageParser()
    parser.feed(html)
    return html, parser


# ---------------------------------------------------------------- F1 Pflichtinhalt
def check_content(root: Path) -> list[str]:
    html, page = _load(root)
    text = page.visible_text
    errors = [
        f"[F1] Pflichtinhalt fehlt {key}: {expected!r}"
        for key, expected in REQUIRED_CONTENT.items()
        if _norm(expected) not in text
    ]
    lowered = html.lower()
    errors += [
        f"[F1] Erfundenes Versprechen/Tracker gefunden: {claim!r}"
        for claim in FORBIDDEN_CLAIMS
        if claim.lower() in lowered
    ]
    return errors


# ---------------------------------------------------------------- F2 Kontakt & Navigation
def check_contact_and_navigation(root: Path) -> list[str]:
    _, page = _load(root)
    errors: list[str] = []

    mailtos = [a for a in page.anchors if a["href"].lower().startswith("mailto:")]
    if not any(a["href"] == CONTACT_MAILTO and CONTACT_LABEL in _norm(a["text"]) for a in mailtos):
        errors.append(f"[F2] Kein Link '{CONTACT_LABEL}' mit Ziel {CONTACT_MAILTO}")
    for a in mailtos:
        if a["href"] != CONTACT_MAILTO:
            errors.append(f"[F2] Falsches Kontaktziel: {a['href']!r} (erwartet {CONTACT_MAILTO})")

    nav_targets = {a["href"] for a in page.anchors if a["in_nav"]}
    for anchor in (SERVICES_ANCHOR, CONTACT_ANCHOR):
        if f"#{anchor}" not in nav_targets:
            errors.append(f"[F2] Navigation (<nav>) enthaelt keinen Link auf #{anchor}")
        if anchor not in page.ids:
            errors.append(f"[F2] Sprungziel id=\"{anchor}\" existiert nicht")

    for a in page.anchors:
        href = a["href"]
        if href.startswith("#") and len(href) > 1 and unquote(href[1:]) not in page.ids:
            errors.append(f"[F2] Interner Link {href!r} hat kein Ziel (id fehlt)")
        if href == "#":
            errors.append("[F2] Leerer interner Link href=\"#\"")
    return errors


# ---------------------------------------------------------------- F3 Lokale Verweise & Assets
def _is_external(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.scheme in ("http", "https") or url.startswith("//"))


def check_local_references(root: Path) -> list[str]:
    html, page = _load(root)
    errors: list[str] = []
    refs = [url for _, url in page.assets] + [a["href"] for a in page.anchors]
    for url in refs:
        if not url or url.startswith(("#", "mailto:", "tel:")):
            continue
        if _is_external(url):
            errors.append(f"[F3] Externe Abhaengigkeit nicht erlaubt: {url!r}")
            continue
        local = urlparse(url).path
        if local.lower().endswith(tuple(FORBIDDEN_PHP_EXTENSIONS)):
            errors.append(f"[F3] PHP-/Server-Endpunkt referenziert: {url!r}")
        target = (root / unquote(local)).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            errors.append(f"[F3] Verweis verlaesst den Produkt-Checkout: {url!r}")
            continue
        if not target.is_file():
            errors.append(f"[F3] Lokales Asset/Verweis existiert nicht: {url!r}")

    if not any(tag == "link" and url.endswith(".css") for tag, url in page.assets):
        errors.append("[F3] Kein lokales Stylesheet eingebunden")

    lowered = html.lower()
    errors += [f"[F3] Server-Code-Marker gefunden: {m!r}" for m in FORBIDDEN_SERVER_MARKERS if m in lowered]
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in FORBIDDEN_PHP_EXTENSIONS:
            errors.append(
                f"[F3] PHP-/Legacy-Datei im Produkt ({path.relative_to(root)}): "
                "CVE-2026-109618 / CVE-2026-109619 Angriffsflaeche"
            )
    return errors


# ---------------------------------------------------------------- F4 Bedienbarkeit (statisch)
def check_usability_static(root: Path) -> list[str]:
    _, page = _load(root)
    errors: list[str] = []
    if not _norm(page.title):
        errors.append("[F4] Dokumenttitel <title> fehlt oder ist leer")
    if page.html_lang.lower() != "de":
        errors.append(f"[F4] <html lang> muss 'de' sein (gefunden: {page.html_lang!r})")
    if not page.has_viewport:
        errors.append("[F4] <meta name=\"viewport\"> fehlt (Voraussetzung fuer 375 px)")
    if page.headings.count(1) != 1:
        errors.append(f"[F4] Genau eine <h1> erwartet (gefunden: {page.headings.count(1)})")
    for prev, cur in zip(page.headings, page.headings[1:]):
        if cur > prev + 1:
            errors.append(f"[F4] Ueberschriftenebene uebersprungen: h{prev} -> h{cur}")
            break
    errors += [f"[F4] Bild ohne alt-Attribut: {src!r}" for src in page.images_without_alt]

    css_path = root / "styles.css"
    if css_path.is_file():
        css = css_path.read_text(encoding="utf-8")
        if ":focus-visible" not in css and ":focus" not in css:
            errors.append("[F4] Kein sichtbarer Tastaturfokus (:focus-visible) in styles.css")
        if re.search(r"outline\s*:\s*(none|0)\s*;", css) and ":focus-visible" not in css:
            errors.append("[F4] Fokusrahmen wird entfernt, ohne :focus-visible-Ersatz")
    return errors


FAMILIES = {
    "F1 Pflichtinhalt (AC-01..AC-04)": check_content,
    "F2 Kontakt & Navigation (AC-04, AC-05)": check_contact_and_navigation,
    "F3 Lokale Verweise & Assets / PHP-frei (AC-05, AC-08)": check_local_references,
    "F4 Bedienbarkeit statisch (AC-06/AC-07)": check_usability_static,
}


def verify_website(base_dir: Path | None = None) -> dict[str, list[str]]:
    root = (base_dir or Path(__file__).resolve().parent).resolve()
    if not (root / "index.html").is_file():
        return {name: ["index.html fehlt"] for name in FAMILIES}
    return {name: fn(root) for name, fn in FAMILIES.items()}


def _assert_family(name: str) -> None:
    errors = verify_website()[name]
    assert not errors, f"{name} fehlgeschlagen:\n- " + "\n- ".join(errors)


def test_f1_content():
    _assert_family("F1 Pflichtinhalt (AC-01..AC-04)")


def test_f2_contact_navigation():
    _assert_family("F2 Kontakt & Navigation (AC-04, AC-05)")


def test_f3_local_references_assets():
    _assert_family("F3 Lokale Verweise & Assets / PHP-frei (AC-05, AC-08)")


def test_f4_usability_static():
    _assert_family("F4 Bedienbarkeit statisch (AC-06/AC-07)")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    results = verify_website()
    failed = False
    for family, errs in results.items():
        status = "PASSED" if not errs else f"FAILED ({len(errs)})"
        print(f"{status:<12} {family}")
        for err in errs:
            print(f"             - {err}")
        failed = failed or bool(errs)
    print("ERGEBNIS: " + ("FEHLGESCHLAGEN" if failed else "ALLE PRUEFFAMILIEN BESTANDEN"))
    sys.exit(1 if failed else 0)
