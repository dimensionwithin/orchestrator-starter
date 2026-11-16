Auftrag demo-1 — Rechenskript mit zwei Tests. AENDERND, ohne Commit.
MODELL: <Modell>      EFFORT: medium      ZEITSPERRE: keine
ORCHESTRATOR: demo
Belegung: keine (Uebung, ein einziger Nutzer)
DEPLOY: kein Deploy
Grundregeln: <Berichte-Ordner>\regeln\grundregeln-auftraege.md gelten

WARUM
ENDZUSTAND (Sicht des Nutzers): Im Arbeitsordner liegt rechner.py mit add und sub, und zwei Tests laufen gruen.
WARUM DIESES MODELL
Stufe 1 der Routing-Tabelle (zwei kleine Dateien), unter 10 Antworten.
REPO-ZUGRIFF
SCHREIBEND nur <Arbeitsordner>\rechner.py, <Arbeitsordner>\test_rechner.py, <Berichte-Ordner>\demo-1-bericht.md. Alles andere KEIN ZUGRIFF.
WAS GETAN WIRD
1. test_rechner.py mit test_add (add(2, 3) ist 5) und test_sub (sub(5, 3) ist 2) schreiben und ausfuehren: beide rot.
2. rechner.py mit add(a, b) und sub(a, b) schreiben.
3. Im Arbeitsordner python -m unittest ausfuehren: Ran 2 tests, OK.
PRUEFUNG
Ran 2 tests, OK; der Bericht nennt die Ausgabe.
BERICHT
<Berichte-Ordner>\demo-1-bericht.md, oben Kurzfassung.
ENDE AUFTRAG demo-1
