# Skripte: post-neu.py (neue Post) und marker.py (Marker)

Die Skripte gehoeren zum Skill `orchestrator-starter`; `post-neu.py` wird nur gebraucht, wenn mehrere Orchestrator-Chats
einander ueber Dateien schreiben. Sie sind unveraendert aus dem Plugin zu uebernehmen und nutzen nur die
Python-Standardbibliothek.

## Einrichten (einmal)

Das Skript nimmt als Basisordner den **Elternordner seines eigenen Ordners**. Liegt es im Plugin, waere das der
Plugin-Ordner. Darum: Ordner `setup-post` im Berichte-Ordner anlegen und das Skript dorthin kopieren:

    <BERICHTE>\setup-post\post-neu.py

Der Basisordner ist dann `<BERICHTE>`. Die erste Ausgabezeile von `post-neu.py` (`post-neu: Berichte-Ordner <Pfad>`) und von
`marker.py` (`marker: Berichte-Ordner <Pfad>`) nennt den Ordner, den das Skript benutzt: Stimmt er nicht, liegt das Skript am
falschen Ort (zum Beispiel noch im Plugin-Ordner), und die Marken landen dort. Dort liegen `RUNDSCHREIBEN.md` (Eintraege an alle) und der Ordner `post\`
mit den Dateien `VON-<Kuerzel>.md`; die Lesemarken schreibt das Skript selbst nach `post\gelesen\<KUERZEL>.txt`.

## Aufruf

Windows: `python <BERICHTE>\setup-post\post-neu.py <Kuerzel>`
Linux/macOS: `python3 <BERICHTE>/setup-post/post-neu.py <Kuerzel>`

- Liest `RUNDSCHREIBEN.md` und `post\VON-*.md` (ohne die eigene VON-Datei) und gibt jeden Eintrag aus, der an dein
  Kuerzel oder `alle` geht und neuer ist als deine Lesemarke. Aelteste zuerst.
- Danach setzt es die Lesemarke auf jetzt. Du schreibst keine Lesemarke von Hand.
  Zeile 1 der Marke bleibt `JJJJ-MM-TT HH:MM`; darunter stehen `#gezeigt-ab-minute` und die schon gezeigten Eintraege
  dieser Minute. So geht ein Eintrag in genau der Minute der Marke nicht verloren und kommt nicht doppelt.
  Alte Marken (nur Zeile 1) bleiben gueltig.
- `--nur-zeigen`: ausgeben, aber Lesemarke nicht aendern. `--stunden N`: Rueckschau, wenn die Lesemarke fehlt (Vorgabe 24).
- Letzte Zeile: `post-neu: <n> neu fuer <KUERZEL> seit <Marke>; Lesemarke jetzt <neu>`. Bei 0 steht (nach der Zeile mit dem
  Berichte-Ordner) nur sie da.
- Eine Zeile, die mit `## ` beginnt, aber kein lesbarer Kopf ist (zum Beispiel mit normalem Bindestrich `-` statt des langen
  Gedankenstrichs `—`), meldet das Skript mit Dateiname und Zeilennummer (`post-neu: VON-A.md, Zeile 5: Kopfzeile nicht
  lesbar: ...`). Dieser Eintrag wird nicht eingelesen, und die Lesemarke wird in diesem Lauf **nicht** gesetzt, damit nichts
  still verloren geht: Korrigiere die Zeile, dann laeuft der naechste Aufruf normal. Das gilt fuer jede Zeile mit `## ` in
  den gelesenen Dateien; Zwischenueberschriften im Text eines Eintrags schreibst du mit `###`.

## Eintragsformat

Jeder Eintrag beginnt mit einem Kopf `## TT.MM.JJJJ HH:MM — an <Kuerzel>[, <Kuerzel>] — <Betreff>` (langer Gedankenstrich;
mit normalem Bindestrich erkennt das Skript den Kopf nicht, meldet die Zeile und setzt die Lesemarke nicht).
Ein Kopf ohne Uhrzeit (`## TT.MM.JJJJ — an …`) zaehlt als 00:00 des Tages. Ein Eintrag geht an jedes genannte Kuerzel
oder an `alle`. **Die Uhrzeit wird als Berliner Ortszeit gelesen** (das Skript vergleicht sie mit der Berliner Zeit):
Eintraege in dieser Zeit schreiben, sonst erscheinen sie zu frueh oder zu spaet.

## Tests

Fuer `post-neu.py` liegt `test_post_neu.py` bei (zwei Tests: Kopfzeile mit Bindestrich, Ausgabe des Berichte-Ordners), fuer
`marker.py` `test_marker.py`; zusammen sechs Tests mit `python -m unittest` (Linux/macOS: `python3`) im Ordner `scripts\`. Eine
kurze Probe von Hand mit Platzhalter-Ordner: Wegwerfordner anlegen, darin `setup-post\post-neu.py` und `post\VON-A.md` mit einem Eintrag
`## 01.01.2030 12:00 — an B — Probe`, dann `python setup-post\post-neu.py B --nur-zeigen` im Wegwerfordner ausfuehren.

## marker.py: Marker "wartet auf dich" setzen

Gehoert zum optionalen Leitstand (Anleitung: [leitstand.md](../anleitungen/leitstand.md)). Einmal unveraendert nach
`<BERICHTE>\setup-post\` kopieren, neben `post-neu.py`; nur Python-Standardbibliothek.

    python <BERICHTE>\setup-post\marker.py <Kuerzel> "Kurztext"      etwas wartet auf den Nutzer
    python <BERICHTE>\setup-post\marker.py <Kuerzel> --keine         nichts ist offen

Das Skript schreibt `<BERICHTE>\leitstand\wartet-<Kuerzel>.txt` (Zeile 1 Zeitstempel, Zeile 2 Kurztext) und nennt in der
ersten Ausgabezeile den benutzten Berichte-Ordner. Beginnt der Kurztext mit `-`, steht `--` davor
(`marker.py <Kuerzel> -- "-Text"`); ohne `--` bricht das Skript mit einem Hinweis darauf ab und schreibt nichts. Tests:
siehe oben (`python -m unittest` im Ordner `scripts\`, Wegwerfordner).
