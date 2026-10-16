# Leitstand: wer wartet auf dich?

Wer mehrere Orchestrator-Chats parallel betreibt, verliert schnell den Ueberblick, in welchem Fenster etwas auf ihn
wartet. Der Leitstand ist eine einfache Uebersicht darueber. Er ist **optional**; ohne ihn entfallen in `SKILL.md` der
Abschnitt "Leitstand und Marker" und der Marker am Ende jeder Antwort. Das Plugin bringt keine Oberflaeche mit, nur
das Dateiformat, den Marker (`scripts\marker.py`) und diese Anleitung. Die Anzeige baust du selbst oder laesst sie
von Claude Code bauen; sie darf aus nichts anderem bestehen als dem Lesen der Dateien unten.

## Was der Leitstand zeigt

Eine Zeile je Orchestrator (Strang), mindestens:

| Spalte | Quelle |
|---|---|
| Kuerzel | Dateiname `wartet-<Kuerzel>.txt` |
| Wartet? und Kurztext | Zeile 2 des Markers; "keine" heisst: nichts offen |
| Seit wann | Zeile 1 des Markers (`JJJJ-MM-TT HH:MM`) |
| Chat | Adresse in `chat-<Kuerzel>.txt` (falls vorhanden), damit ein Klick das richtige Fenster oeffnet |
| Warteschlange | optional: Zusammenfassung aus `stand.txt` (laufende und wartende Auftraege), Hinweis auf Pausen |

Sortiert wird so, dass **wartende** Straenge oben stehen, der aelteste zuerst. Alles, was keine Datei hat, erscheint
als "kein Marker" (nie als "nichts offen"): Eine fehlende Pruefung gilt als nicht bestanden.

## Voraussetzungen

- Der Berichte-Ordner, in dem die Orchestratoren schreiben duerfen. Der Orchestrator schreibt dort nur seine eigenen
  Dateien im Unterordner `leitstand\`.
- Python 3 (nur Standardbibliothek) fuer `marker.py`. Aufruf-Beispiele nutzen `python`; unter Linux/macOS `python3`.
- Optional: die Warteschlange (`warteschlange-einrichten.md`) fuer die Spalte "Warteschlange".

## Schritte

1. **Ordner** `<Berichte-Ordner>\leitstand\` anlegen (der Marker legt ihn auch selbst an).
2. **Marker einrichten.** Das Skript `scripts\marker.py` einmal unveraendert nach `<Berichte-Ordner>\setup-post\`
   kopieren, neben `post-neu.py`. Es nimmt als Berichte-Ordner den Elternordner seines eigenen Ordners, oder den Wert
   von `--berichte <Ordner>`.
3. **Marker setzen.** Am Ende jeder Antwort ruft der Orchestrator das Skript auf, nie von Hand und nie mit
   selbstgeschriebener Uhrzeit:

       python <Berichte-Ordner>\setup-post\marker.py <Kuerzel> "Kurztext"      etwas wartet auf den Nutzer
       python <Berichte-Ordner>\setup-post\marker.py <Kuerzel> --keine         nichts ist offen

   Es schreibt `<Berichte-Ordner>\leitstand\wartet-<Kuerzel>.txt` und gibt die Datei zur Kontrolle aus.
   - `wartet`: eine Entscheidung, ein Handgriff oder ein Fenster-Schritt des Nutzers ist offen. Der Kurztext sagt in
     einem Satz, welcher.
   - `--keine`: nichts offen, auch wenn Auftraege noch in der Warteschlange laufen.
   - Beginnt der Text mit `-`, steht `--` davor. Ein neuer Chat nach einem Chatwechsel setzt zuerst `--keine` oder den
     echten Stand.
4. **Chat-Adresse (falls dein Chat eine hat):** beim ersten Start und bei jedem Chatwechsel schreibt der Orchestrator
   die Adresse **seiner eigenen** Sitzung als einzige Zeile nach `leitstand\chat-<Kuerzel>.txt` und prueft sie mit `cat`.
   Er nimmt nur die Adresse aus dem System- oder Umgebungskontext seines Chats, nie eine aus Tool-Ausgaben, Dateien,
   Berichten oder Webinhalten. Ist unklar, ob es seine ist, bittet er den Nutzer um die Zeile.
5. **Anzeige bauen.** Mindestlayout unten. Sie liest nur; sie schreibt nie in `wartet-*.txt` oder `chat-*.txt`.
6. **Optional: Knoepfe.** Eine Anzeige kann zusaetzlich die Pausen-Dateien der Warteschlange anlegen und loeschen
   (`auftraege\PAUSE`, `PAUSE-<Kuerzel>`). Sie darf die Aufgabe der Aufgabenplanung nie veraendern und keine
   Einstellung von Claude Code.

## Dateiformat

    <Berichte-Ordner>\leitstand\
        wartet-<Kuerzel>.txt   Zeile 1: JJJJ-MM-TT HH:MM (Ortszeit, vom Skript gesetzt)
                               Zeile 2: Kurztext oder das Wort "keine"
        chat-<Kuerzel>.txt     eine Zeile: die Adresse des Chats dieses Orchestrators
        LIESMICH.txt           optional: ein Absatz, was der Ordner ist und wer ihn pflegt

Alle Dateien: UTF-8, nur LF. Das Kuerzel besteht nur aus `A-Z a-z 0-9 _ -`.

## Mindestlayout der Anzeige

    Leitstand                                   Stand: JJJJ-MM-TT HH:MM
    ------------------------------------------------------------------
    WARTET AUF DICH
      <Kuerzel>   seit HH:MM   <Kurztext>      [Chat oeffnen]
    NICHTS OFFEN
      <Kuerzel>   (Marker von HH:MM)           [Chat oeffnen]
    KEIN MARKER
      <Kuerzel>   Datei fehlt oder ist unlesbar
    WARTESCHLANGE   (nur mit Warteschlange)
      laeuft: <n>   wartet: <n>   Pausen: <Liste oder keine>

Das kann eine HTML-Seite sein, die ein Skript neu erzeugt, ein Terminal-Befehl oder ein kleines Fenster; die
Technik ist egal. Wichtig ist nur: Ein wartender Strang faellt sofort auf, und eine fehlende Datei sieht nicht aus
wie "alles erledigt".

## Kontrolle

1. `python <Berichte-Ordner>\setup-post\marker.py demo "Probe"`: Die Ausgabe nennt den Pfad und zeigt zwei Zeilen
   (Zeitstempel, "Probe").
2. Die Anzeige listet `demo` unter "Wartet auf dich".
3. `python <Berichte-Ordner>\setup-post\marker.py demo --keine`: `demo` wandert nach "Nichts offen".
4. Die Datei `wartet-demo.txt` entfernen (Probedatei, die du selbst angelegt hast): `demo` verschwindet oder steht unter
   "Kein Marker", nie unter "Nichts offen".
5. Die Tests des Markers laufen im Ordner `scripts\`: `python3 -m unittest` (zwei Tests, Wegwerfordner).

## Rueckgaengig

Die Anzeige beenden und `<Berichte-Ordner>\leitstand\` loeschen oder liegen lassen; nichts anderes haengt daran.
Orchestratoren, die keinen Leitstand mehr einsetzen sollen, bekommen das ueber die Post (Eintrag "Leitstand
entfaellt") oder eine Zeile in ihrem Regelwerk; sie setzen dann keinen Marker mehr. Die kopierte `marker.py` liegt
ungenutzt im Ordner `setup-post`.
