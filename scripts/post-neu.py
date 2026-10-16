#!/usr/bin/env python3
"""post-neu.py - liefert die neue Post an ein Orchestrator-Fenster und setzt die Lesemarke.

Aufruf: post-neu.py <KUERZEL> [--nur-zeigen] [--stunden N]
Basisordner = Elternordner dieses Skript-Ordners (enthaelt RUNDSCHREIBEN.md und post/).
Nur Standardbibliothek; laeuft unter Windows-Python und Linux-python3.
"""
import argparse
import datetime as dt
import os
import re
import sys

KOPF = re.compile(
    r"^##\s+(\d{2})\.(\d{2})\.(\d{4})(?:\s+(\d{1,2}):(\d{2}))?\s+—\s+an\s+(.*?)\s+—\s*(.*)$"
)
MARKE_FORMAT = "%Y-%m-%d %H:%M"
MARKE_V2 = "#gezeigt-ab-minute"


def letzter_sonntag(jahr, monat):
    d = dt.date(jahr, monat, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def berlin_regel(utc_dt):
    """Europe/Berlin ohne tzdata: Sommerzeit von letztem Sonntag Maerz 01:00 UTC
    bis letztem Sonntag Oktober 01:00 UTC. Gibt naive Berliner Ortszeit zurueck."""
    u = utc_dt.replace(tzinfo=None)
    beginn = dt.datetime.combine(letzter_sonntag(u.year, 3), dt.time(1, 0))
    ende = dt.datetime.combine(letzter_sonntag(u.year, 10), dt.time(1, 0))
    stunden = 2 if beginn <= u < ende else 1
    return u + dt.timedelta(hours=stunden)


def berlin_jetzt(utc_dt=None):
    """Aktuelle Berliner Ortszeit (naiv). zoneinfo, sonst Rechner-Ortszeit bei +01/+02, sonst Regel."""
    if utc_dt is None:
        utc_dt = dt.datetime.now(dt.timezone.utc)
    try:
        from zoneinfo import ZoneInfo
        return utc_dt.astimezone(ZoneInfo("Europe/Berlin")).replace(tzinfo=None)
    except Exception:
        pass
    lokal = utc_dt.astimezone()
    abstand = lokal.utcoffset()
    if abstand in (dt.timedelta(hours=1), dt.timedelta(hours=2)):
        return lokal.replace(tzinfo=None)
    return berlin_regel(utc_dt)


def lies_text(pfad):
    with open(pfad, "r", encoding="utf-8-sig", errors="replace", newline=None) as f:
        return f.read()


def eintraege(pfad, quelle):
    """Zerlegt eine Datei in (zeit, empfaenger_text, kopf_ohne_##, text, quelle)."""
    ergebnis = []
    aktuell = None
    for zeile in lies_text(pfad).split("\n"):
        zeile = zeile.rstrip("\r")
        if zeile.startswith("## "):
            if aktuell:
                ergebnis.append(aktuell)
            m = KOPF.match(zeile)
            if m:
                tt, mm, jjjj, hh, mi, empf, _ = m.groups()
                try:
                    zeit = dt.datetime(int(jjjj), int(mm), int(tt), int(hh or 0), int(mi or 0))
                except ValueError:
                    m = None
            if m:
                aktuell = {"zeit": zeit, "empf": empf, "kopf": zeile[3:].strip(),
                           "zeilen": [], "quelle": quelle}
            else:
                aktuell = None
        elif aktuell is not None:
            aktuell["zeilen"].append(zeile)
    if aktuell:
        ergebnis.append(aktuell)
    for e in ergebnis:
        z = e["zeilen"]
        while z and (not z[-1].strip() or z[-1].strip() == "---"):
            z.pop()
        while z and not z[0].strip():
            z.pop(0)
        e["text"] = "\n".join(z)
    return ergebnis


def ist_empfaenger(empf_text, kuerzel):
    woerter = {w.casefold() for w in re.findall(r"\w+", empf_text)}
    return kuerzel.casefold() in woerter or "alle" in woerter


def lies_marke_voll(pfad):
    """Gibt (zeit, gezeigt) zurueck. Alte Marke (nur Zeile 1): gezeigt = None, es zaehlt
    'neuer als zeit'. Neue Marke (Zeile 2 = MARKE_V2): gezeigt = Liste der Eintrags-IDs, die in
    Minute 'zeit' oder spaeter schon gezeigt wurden, es zaehlt 'zeit oder spaeter'.
    Unlesbar: (None, None)."""
    try:
        zeilen = lies_text(pfad).strip().splitlines()
        zeit = dt.datetime.strptime(zeilen[0].strip(), MARKE_FORMAT)
    except Exception:
        return None, None
    if len(zeilen) > 1 and zeilen[1].strip() == MARKE_V2:
        return zeit, [z.strip() for z in zeilen[2:] if z.strip()]
    return zeit, None


def lies_marke(pfad):
    return lies_marke_voll(pfad)[0]


def schreibe_marke(pfad, zeit, gezeigt=()):
    """Zeile 1 bleibt das alte Format (alte Leser sehen nur sie); danach MARKE_V2 und die IDs."""
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    tmp = pfad + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(zeit.strftime(MARKE_FORMAT) + "\n" + MARKE_V2 + "\n")
        for eid in gezeigt:
            f.write(eid + "\n")
    os.replace(tmp, pfad)


def eintrag_id(e):
    return e["quelle"] + "|" + e["kopf"]


def sammle(basis, kuerzel, seit, einschliesslich=False):
    quellen = [("RUNDSCHREIBEN.md", os.path.join(basis, "RUNDSCHREIBEN.md"))]
    post = os.path.join(basis, "post")
    if os.path.isdir(post):
        for name in sorted(os.listdir(post)):
            if name.startswith("VON-") and name.endswith(".md") \
                    and name[4:-3].casefold() != kuerzel.casefold():
                quellen.append((name, os.path.join(post, name)))
    treffer = []
    for name, pfad in quellen:
        if not os.path.isfile(pfad):
            continue
        for e in eintraege(pfad, name):
            if (e["zeit"] >= seit if einschliesslich else e["zeit"] > seit) \
                    and ist_empfaenger(e["empf"], kuerzel):
                treffer.append(e)
    treffer.sort(key=lambda e: e["zeit"])  # stabil: gleiche Zeit behaelt Dateireihenfolge
    return treffer


def lauf(basis, kuerzel, nur_zeigen=False, stunden=24, jetzt=None, ausgabe=None):
    """Gibt die Ausgabe als Text zurueck (und setzt die Lesemarke, ausser nur_zeigen)."""
    jetzt = jetzt or berlin_jetzt()
    jetzt = jetzt.replace(second=0, microsecond=0)
    marke_pfad = os.path.join(basis, "post", "gelesen", kuerzel + ".txt")
    marke, gezeigt = lies_marke_voll(marke_pfad) if os.path.isfile(marke_pfad) else (None, None)
    seit = marke if marke is not None else jetzt - dt.timedelta(hours=stunden)
    # Neue Marke: Eintraege der Marken-Minute mitnehmen und schon Gezeigte ueber die ID aussortieren.
    kandidaten = sammle(basis, kuerzel, seit, einschliesslich=gezeigt is not None)
    offen = {}
    for eid in gezeigt or ():
        offen[eid] = offen.get(eid, 0) + 1
    treffer = []
    for e in kandidaten:
        if offen.get(eintrag_id(e), 0) > 0:
            offen[eintrag_id(e)] -= 1
        else:
            treffer.append(e)
    teile = []
    for e in treffer:
        teile.append("### %s — %s\n%s\n" % (e["quelle"], e["kopf"], e["text"]))
    teile.append("post-neu: %d neu fuer %s seit %s; Lesemarke jetzt %s" % (
        len(treffer), kuerzel, seit.strftime(MARKE_FORMAT),
        "unveraendert (--nur-zeigen)" if nur_zeigen else jetzt.strftime(MARKE_FORMAT)))
    if not nur_zeigen:
        # Alles ab der neuen Marken-Minute (gezeigt jetzt oder schon frueher) merken, damit ein
        # spaeter in dieser Minute geschriebener Eintrag erscheint, ein gezeigter aber nicht doppelt.
        schreibe_marke(marke_pfad, jetzt, [eintrag_id(e) for e in kandidaten if e["zeit"] >= jetzt])
    return "\n".join(teile)


def main(argv=None):
    p = argparse.ArgumentParser(description="Neue Post fuer ein Orchestrator-Fenster")
    p.add_argument("kuerzel")
    p.add_argument("--nur-zeigen", action="store_true")
    p.add_argument("--stunden", type=float, default=24)
    a = p.parse_args(argv)
    if not re.fullmatch(r"[A-Za-z0-9_-]+", a.kuerzel):
        print("post-neu: ungueltiges Kuerzel", file=sys.stderr)
        return 1
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    basis = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(lauf(basis, a.kuerzel.upper(), a.nur_zeigen, a.stunden))
    return 0


if __name__ == "__main__":
    sys.exit(main())
