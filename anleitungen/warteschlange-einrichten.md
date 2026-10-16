# Warteschlange einrichten

Die Warteschlange startet fertige Auftraege von selbst, auch wenn du nicht am Rechner sitzt. Das Plugin bringt **kein**
Programm dafuer mit, nur diese Anleitung. Du richtest sie selbst ein; ein Orchestrator tut das nie. In diesem Text
heisst der Berichte-Ordner `<Berichte-Ordner>` (derselbe wie in der Plugin-Einstellung `berichte_ordner`) und der
Ordner fuer das Programm `<Warteschlange-Ordner>` (z. B. `<Berichte-Ordner>\setup-warteschlange`).

## Voraussetzungen

- Claude Code ist installiert und angemeldet, und `claude -p "Hallo"` laeuft in einem normalen Terminal durch.
  Pruefe die Schalter deiner Version mit `claude --help`: gebraucht werden `-p`/`--print`, `--model`, `--effort`,
  `--permission-mode` und `--permission-prompts` (alle in der Hilfe der getesteten Version vorhanden).
- Python 3 (nur Standardbibliothek) fuer das kleine Programm, das die Reihe abarbeitet. Du kannst es von Claude Code
  nach der Beschreibung unten bauen lassen; es ist nicht Teil des Plugins.
- Windows: Aufgabenplanung (in jeder Windows-Version dabei) und PowerShell. Linux/macOS: siehe Abschnitt "Alternative".
- **Die Rechte eines Laufs bestimmst du.** Ein Lauf ohne Rueckfrage tut nur, was deine Claude-Code-Einstellungen
  erlauben; alles andere wird abgelehnt. Das Plugin liefert dafuer keine Erlaubnisregeln. Lege sie selbst fest und
  lies sie vor dem ersten Lauf noch einmal durch. Nimm nie einen Schalter, der alle Pruefungen abschaltet, nur damit
  ein Lauf durchgeht.

## Schritt 1: Ordner anlegen

Unter `<Berichte-Ordner>` legst du an:

    auftraege\bereit\        fertige Auftraege, warten auf den Start
    auftraege\laeuft\        laufende Auftraege
    auftraege\erledigt\      Lauf beendet (Exit 0) und Bericht vorhanden
    auftraege\gescheitert\   Lauf gescheitert; daneben <Kennung>.grund.txt mit dem Grund
    post\                    Rueckmeldungen an die Orchestratoren (VON-WARTESCHLANGE.md)
    <Warteschlange-Ordner>\  das Programm, die Zahl parallel.txt, die Statusdatei stand.txt, Protokolle

Ein Auftrag wandert nur zwischen diesen Ordnern. **Nichts wird geloescht oder ueberschrieben**: gibt es den Namen im
Zielordner schon, bekommt die Datei einen Zeitstempel im Namen.

## Schritt 2: Das Programm (Beschreibung zum Selberbauen)

Ein Programm `warteschlange.py` mit einem **Lauf pro Aufruf** (kein Dauerprozess; die Aufgabenplanung ruft es
regelmaessig). Pfade nimmt es aus Parametern oder liegt im Ordner des Berichte-Ordners, nie fest einkompiliert.
Ein Lauf:

1. **Pausen-Datei:** Liegt `auftraege\PAUSE`, schreibt der Lauf nur die Statusdatei und startet nichts.
2. **Aufraeumen:** Fuer jeden Auftrag in `laeuft\` gibt es eine Datei `<Kennung>.pid` (Prozessnummer, Startzeit). Ist
   der Prozess weg, geht der Auftrag nach `gescheitert\` mit Grund "abgebrochen, Runner verschwunden".
3. **Waehlen:** Aus `bereit\` nur Dateien, die laenger als eine Minute unveraendert sind (sie werden sonst evtl. noch
   geschrieben), in der Reihenfolge ihres Alters. Pruefen je Auftrag: erste Zeile `Auftrag <Kennung> — …`, letzte
   nicht leere Zeile `ENDE AUFTRAG <Kennung>`, `MODELL:` und `EFFORT:` bekannt. Sonst sofort nach `gescheitert\`.
4. **Vertraeglichkeit:** Siehe "Regeln der Reihen" unten. Hoechstens so viele Auftraege gleichzeitig, wie
   `parallel.txt` sagt (laufende zaehlen mit).
5. **Starten:** Auftrag nach `laeuft\` verschieben, `<Kennung>.pid` exklusiv anlegen (schlaegt das fehl, hat ihn
   schon ein anderer Lauf genommen), dann nicht-interaktiv starten:

       claude -p "<Startauftrag>" --permission-mode <Modus> --permission-prompts none --model <Modell-ID> --effort <Effort>

   Der Startauftrag verweist auf die Datei in `laeuft\` und sagt: unbeaufsichtigt, keine Rueckfragen, Technisch
   Unklares auslegen und im Bericht melden, bei Sicherheitseinstellungen, fremden Prozessen oder einer Kollision mit
   anderer Arbeit sauber anhalten, erst enden, wenn der Bericht geschrieben ist (**der Prozess endet mit der Antwort**).
   `<Modus>` und die Rechte sind deine Entscheidung (siehe Voraussetzungen). Modell und Effort kommen aus dem
   Auftragskopf; ein unbekannter Name ist ein Fehler, nie ein stilles Standardmodell. Pro Auftrag eine Zeitgrenze
   (z. B. 8 Stunden); danach den ganzen Prozessbaum beenden, nicht nur den Elternprozess. Ausgabe nach
   `<Warteschlange-Ordner>\logs\<Kennung>-<Zeit>.log`.
6. **Abschliessen:** **erledigt** = Exit 0 **und** `<Berichte-Ordner>\<Kennung>-bericht.md` ist neuer als der Start;
   sonst **gescheitert** (mit Grund-Datei). Danach eine Zeile Post an den Orchestrator aus `ORCHESTRATOR:` im Kopf in
   `post\VON-WARTESCHLANGE.md` (im Eintragsformat der Post, siehe `scripts\LIESMICH.md`). Zuletzt die `.pid` loeschen.
7. **Statusdatei** `stand.txt` bei jedem Lauf neu schreiben (atomar: erst temporaer, dann ersetzen): LAEUFT (Kennung,
   Repos, seit wann) und WARTET (Kennung, worauf), dazu eine Zeile, falls eine Pause liegt.

Zwei Laeufe duerfen sich nicht ueberholen: Die Auswahl (Schritt 3 bis 5) laeuft unter einer kurzen exklusiven Sperrdatei
(`auswahl.lock`, aelter als 2 Minuten gilt als verwaist). Dateien, die mehrere Laeufe beschreiben (Protokoll, Post),
nur anhaengen bzw. atomar ersetzen. Fuer jedes Verhalten sollte ein Test dasein; lass dir zuerst einen Probemodus
bauen (`--probe`: zeigt je Auftrag, ob er starten wuerde oder worauf er wartet, und aendert nichts).

## Regeln der Reihen

- Mit Belegung (siehe `belegung.md`): Jedes Projekt hat seine eigene Reihe nach Alter der Dateien. Ein Auftrag startet,
  wenn er **in jedem seiner Projekte vorn** ist und **jedes seiner Projekte frei** ist (kein laufender Auftrag und kein
  Eintrag in `belegung\`, der sich nicht vertraegt). Vertraeglich sind nur `lesen` und `lesen`. Ein Auftrag mit
  mehreren Projekten wartet, bis alle frei sind, und niemand ueberholt ihn in diesen Projekten.
- `Belegung: keine (<Grund>)` im Kopf: startet sofort, unabhaengig von den Reihen.
- Fehlt die Zeile `Belegung:` oder ist sie unlesbar, geht der Auftrag nach `gescheitert\`: Unbekannt gilt als nicht
  bestanden, nie als "frei".
- Ohne Belegung (ihr setzt sie nicht ein): eine einzige Reihe nach Alter; setze dann `parallel.txt` auf `1`, wenn
  zwei Auftraege nie gleichzeitig dieselben Dateien anfassen duerfen.
- Kennungen werden nie wiederverwendet. Wer dieselbe Kennung zweimal einreiht, bekommt die Meldung "laeuft schon".
- Feste Zeitfenster (z. B. ein naechtliches Backup) und eine ZEITSPERRE im Auftrag kennt das Programm nur, wenn du
  sie einbaust. Reihe nichts ein, das absehbar hineinfaellt.

## Notbremse

- **Alles anhalten:** leere Datei `auftraege\PAUSE` anlegen. Laufende Auftraege laufen zu Ende, es startet nichts Neues.
  Wieder loeschen setzt fort.
- **Nur einen Strang oder ein Projekt anhalten (optional):** `auftraege\PAUSE-<Kuerzel>` bzw.
  `auftraege\PAUSE-projekt-<Name>`. Pausierte Auftraege bleiben in `bereit\` liegen und blockieren niemanden.
- **Weniger gleichzeitig:** erste Zahl in `<Warteschlange-Ordner>\parallel.txt` (Vorlage: `vorlagen\parallel.txt`).
  Fehlt die Datei oder ist die Zahl ungueltig, nimmt das Programm einen festen Vorgabewert; waehle ihn klein.
  Empfehlung aus der Praxis: **6 gleichzeitig reichen**; mehr bringt kaum Tempo und heizt den Rechner auf (siehe
  `unbeaufsichtigt.md`).
- Nie ein Fenster schliessen und nie einen Prozess nach Namen beenden: Das trifft auch fremde Python- und
  Claude-Prozesse. Beende hoechstens genau die Prozessnummer aus der `.pid`-Datei des Auftrags.

## Schritt 3: Regelmaessig starten (Windows-Aufgabenplanung)

Die Aufgabe ruft das Programm alle 3 Minuten auf und **erlaubt mehrere Instanzen gleichzeitig**, sonst wartet ein
neuer Lauf, bis der lange Lauf des vorigen fertig ist. Beispiel in PowerShell (alle Namen und Pfade sind Platzhalter;
die Cmdlets und Schalter sind geprueft, die Aufgabe selbst ist nicht angelegt worden):

    $aktion = New-ScheduledTaskAction -Execute "<Pfad-zu-pythonw.exe>" `
        -Argument '"<Warteschlange-Ordner>\warteschlange.py" --berichte "<Berichte-Ordner>"'
    $ausloeser = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
        -RepetitionInterval (New-TimeSpan -Minutes 3)
    $einstellungen = New-ScheduledTaskSettingsSet -MultipleInstances Parallel -ExecutionTimeLimit (New-TimeSpan -Hours 9)
    Register-ScheduledTask -TaskName "Auftrags-Warteschlange" -Action $aktion -Trigger $ausloeser -Settings $einstellungen

- `pythonw.exe` (statt `python.exe`) oeffnet kein Konsolenfenster. Gibt es eines in deiner Installation nicht, nimm
  `python.exe` und starte die Aufgabe als "unabhaengig von der Benutzeranmeldung" (Aufgabenplanung, Reiter
  "Allgemein"); dafuer fragt Windows nach deinem Kennwort. Gib es nur dort ein, nie in eine Datei oder einen Auftrag.
- Das Zeitlimit der Aufgabe muss laenger sein als die laengste erlaubte Laufzeit eines Auftrags.
- Dieselbe Einrichtung per Oberflaeche: Aufgabenplanung > Aufgabe erstellen > Trigger "Taeglich", wiederholen alle
  3 Minuten > Aktion "Programm starten" > Reiter Einstellungen: "Falls die Aufgabe bereits ausgefuehrt wird:
  Neue Instanz parallel starten".

### Alternative: Linux (cron) und macOS (launchd)

Nur als Hinweis, hier nicht getestet. Das Programm bleibt dasselbe (die Windows-Teile wie die Prozessverwaltung mit
dem Job-Objekt ersetzt du durch eine Prozessgruppe).
- **cron:** `crontab -e` und eine Zeile `*/3 * * * * python3 <Warteschlange-Ordner>/warteschlange.py --berichte <Berichte-Ordner>`.
  cron startet pro Minute-Treffer einen neuen Prozess; der Programmlauf selbst darf lange dauern.
- **launchd:** eine Datei `~/Library/LaunchAgents/<Name>.plist` mit `ProgramArguments` und `StartInterval` 180, geladen
  mit `launchctl load`. launchd startet keine zweite Instanz, solange die erste laeuft: lass das Programm die
  Auftraege darum in Kindprozessen starten und sich selbst nach dem Start beenden, oder nimm mehrere Aufgaben.

## Kontrolle

1. Lege einen Probeauftrag an: `vorlagen\BEISPIEL-AUFTRAG.md` kopieren, Platzhalter fuellen, Kennung vergeben, nach
   `auftraege\bereit\` legen, `tail -1` zeigt `ENDE AUFTRAG <Kennung>`.
2. Probemodus des Programms laufen lassen: Der Auftrag steht als "wuerde starten" da, die Dateien haben sich nicht
   bewegt.
3. Nach hoechstens drei Minuten (+1 Minute Ruhezeit) steht er in `stand.txt` unter LAEUFT, spaeter liegt er in
   `erledigt\`, und der Bericht `<Berichte-Ordner>\<Kennung>-bericht.md` existiert.
4. Die Post in `post\VON-WARTESCHLANGE.md` hat einen Eintrag "erledigt".
5. Gegenprobe der Notbremse: `auftraege\PAUSE` anlegen, einen zweiten Probeauftrag einreihen: er bleibt in `bereit\`
   und `stand.txt` nennt die Pause. Datei wieder loeschen, er startet.
6. Gegenprobe Scheitern: ein Auftrag ohne letzte Zeile `ENDE AUFTRAG <Kennung>` geht nach `gescheitert\` mit Grund.

Laeuft ein Auftrag nicht an: erst `stand.txt` (worauf er wartet), dann das Protokoll des Programms gezielt mit der
Kennung durchsuchen, dann das Log des Laufs unter `logs\`. Gescheitert: `<Kennung>.grund.txt` und die letzten
Zeilen des Logs lesen, Ursache beheben, mit **neuer** Kennung einreihen (z. B. `<Kennung>b`).

## Rueckgaengig

1. Aufgabe stoppen: `Disable-ScheduledTask -TaskName "Auftrags-Warteschlange"`. Laufende Auftraege laufen zu Ende.
2. Wer sie ganz entfernen will: `Unregister-ScheduledTask -TaskName "Auftrags-Warteschlange" -Confirm:$false`. Das
   betrifft nur diese Aufgabe, keine Einstellung von Claude Code.
3. Die Ordner und alle Auftraege, Berichte und Post bleiben unveraendert liegen; das Programm hat nichts geloescht.
   Auftraege aus `bereit\` startest du dann von Hand wie vorher.
4. Hast du fuer die Warteschlange Erlaubnisregeln in den Claude-Code-Einstellungen eingetragen, nimmst du sie dort
   selbst wieder heraus; das kann dieses Paket nicht fuer dich tun.
