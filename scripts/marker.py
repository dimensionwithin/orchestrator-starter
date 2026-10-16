"""marker.py: setzt den Marker "wartet auf dich" eines Orchestrators im Leitstand.

Aufruf:
  python marker.py <Kuerzel> "Kurztext"      etwas wartet auf den Nutzer
  python marker.py <Kuerzel> --keine         nichts ist offen
  python marker.py --berichte <Ordner> ...   Berichte-Ordner ausdruecklich angeben

Der Berichte-Ordner ist der Parameter --berichte. Ohne ihn gilt der Elternordner des Ordners, in dem dieses Skript
liegt (Skript in <Berichte-Ordner>/setup-post/marker.py, wie post-neu.py).

Geschrieben wird <Berichte-Ordner>/leitstand/wartet-<Kuerzel>.txt, UTF-8, nur LF:
  Zeile 1: JJJJ-MM-TT HH:MM (Ortszeit des Rechners, vom Skript gesetzt, nie von Hand)
  Zeile 2: der Kurztext, oder das Wort "keine"
Zum Schluss wird die Datei zur Kontrolle ausgegeben. Nur Python-Standardbibliothek.
"""
import argparse
import datetime
import os
import pathlib
import re
import sys

KUERZEL_OK = re.compile(r"[A-Za-z0-9_-]+")
KEINE = "keine"
MAX_TEXT = 300


def berichte_ordner(angabe):
    """Der Parameter, sonst der Elternordner des Skriptordners."""
    if angabe:
        return pathlib.Path(angabe)
    return pathlib.Path(__file__).resolve().parent.parent


def marker_text(text, jetzt=None):
    """Inhalt der Marker-Datei. Der Text wird einzeilig und gekuerzt."""
    jetzt = jetzt or datetime.datetime.now()
    einzeilig = " ".join(text.split())[:MAX_TEXT] or KEINE
    return f"{jetzt:%Y-%m-%d %H:%M}\n{einzeilig}\n"


def setze_marker(berichte, kuerzel, text, jetzt=None):
    """Schreibt wartet-<Kuerzel>.txt (atomar ersetzt) und gibt den Pfad zurueck.
    Wirft ValueError bei ungueltigem Kuerzel oder fehlendem Berichte-Ordner."""
    if not KUERZEL_OK.fullmatch(kuerzel):
        raise ValueError(f"Kuerzel '{kuerzel}' darf nur A-Z a-z 0-9 _ - enthalten")
    berichte = pathlib.Path(berichte)
    if not berichte.is_dir():
        raise ValueError(f"Berichte-Ordner fehlt: {berichte}")
    ordner = berichte / "leitstand"
    ordner.mkdir(exist_ok=True)
    ziel = ordner / f"wartet-{kuerzel}.txt"
    tmp = ordner / f"wartet-{kuerzel}.txt.{os.getpid()}.tmp"
    tmp.write_text(marker_text(text, jetzt), encoding="utf-8", newline="\n")
    os.replace(tmp, ziel)
    return ziel


def main(argv=None):
    ap = argparse.ArgumentParser(description="Marker 'wartet auf dich' im Leitstand setzen")
    ap.add_argument("--berichte", help="Berichte-Ordner (Vorgabe: Elternordner dieses Skripts)")
    ap.add_argument("kuerzel")
    ap.add_argument("text", nargs="?", default="", help="Kurztext; beginnt er mit '-', steht -- davor")
    ap.add_argument("--keine", action="store_true", help="nichts ist offen")
    a = ap.parse_args(argv)
    if a.keine == bool(a.text.strip()):
        print("marker: entweder Kurztext oder --keine angeben", file=sys.stderr)
        return 1
    try:
        ziel = setze_marker(berichte_ordner(a.berichte), a.kuerzel, KEINE if a.keine else a.text)
    except (ValueError, OSError) as e:
        print(f"marker: {e}", file=sys.stderr)
        return 1
    print(f"marker: {ziel}")
    print(ziel.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
