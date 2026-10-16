# Regel Auftrags-Warteschlange (optional, zum Skill orchestrator-starter)

Das Plugin bringt **keine** Warteschlange mit. Diese Regel sagt, was du als Orchestrator beachtest, wenn der Nutzer
eine eingerichtet hat. Wie man sie einrichtet, steht in `anleitungen\warteschlange-einrichten.md` im Plugin
(Einrichten, Aendern und Loeschen der zugehoerigen Aufgabe ist Sache des Nutzers, nie deine). Der Skill setzt sie
nirgends voraus; ohne sie startet der Nutzer jeden Auftrag von Hand.

## Was sie tut (der Vertrag, auf den du dich verlaesst)

Ein kleines Programm, das regelmaessig (z. B. alle paar Minuten) laeuft, mit diesem Ordnerbaum unter `<BERICHTE>`:

    auftraege\bereit\       fertige Auftraege, warten auf den Start
    auftraege\laeuft\       laufende Auftraege
    auftraege\erledigt\     Lauf beendet, Bericht vorhanden
    auftraege\gescheitert\  Lauf gescheitert, daneben eine Datei mit dem Grund

Ein Lauf des Programms:
1. Prueft, ob eine Pausen-Datei liegt. Wenn ja: nichts starten.
2. Raeumt tote Laeufe auf (Auftrag steht in `laeuft\`, der Prozess existiert nicht mehr: nach `gescheitert\`).
3. Waehlt Auftraege aus `bereit\`, die sich vertragen, verschiebt sie nach `laeuft\` und startet Claude Code
   nicht-interaktiv mit dem Modell und Effort aus dem Auftragskopf. Obergrenzen fuer Laufzeit und gleichzeitige
   Laeufe sind Sache des Nutzers.
4. Danach je Auftrag: **erledigt**, wenn der Lauf mit Exit 0 endet und `<BERICHTE>\<Kennung>-bericht.md` neu ist;
   sonst **gescheitert**. Das Ergebnis geht als Post an den Orchestrator aus der Zeile `ORCHESTRATOR:`.

Einzelheiten (Reihenfolge, Gleichzeitigkeit, Statusdatei) haengen vom Programm des Nutzers ab. Ist dir etwas unklar, lies
seine Anleitung, rate nicht.

## Pflichten fuer einen Auftrag in `bereit\`

- Dateiname `<Kennung>.md`, erste Zeile `Auftrag <Kennung> — …`, letzte nicht leere Zeile `ENDE AUFTRAG <Kennung>`.
  Nach dem Schreiben mit `tail -1` pruefen. Fehlt die letzte Zeile, scheitert der Auftrag sofort.
- Kopf mit `MODELL:` und `EFFORT:`, dazu `ORCHESTRATOR: <Kuerzel>` fuer die Rueckmeldung. Wo euer Programm es
  verlangt, auch die Zeile `Belegung:`.
- Alles entschieden, keine Anmeldung, kein Handgriff, keine Rueckfrage. Sonst Start von Hand.
- Der Lauf hat nur die Rechte, die der Nutzer in seinen Einstellungen vergeben hat. Brauchst du etwas anderes, schreib
  den Auftrag nicht fuer die Warteschlange, sondern gib ihn von Hand ab.
- Feste Zeitfenster und die ZEITSPERRE kennt die Warteschlange nicht, wenn der Nutzer sie nicht eingebaut hat: nichts
  einreihen, das absehbar hineinfaellt.
- Kennungen nie wiederverwenden. Gescheitert: Ursache beheben, neu einreihen mit neuer Kennung (z. B. `<Kennung>b`).
  Hochstufen des Modells nur bei Scheitern am Koennen, nicht bei Umgebungsfehlern.
- Lies ein Scheitern nach: Post der Warteschlange, dann `head -25` des Berichts (falls es einen gibt) oder die
  Grund-Datei in `gescheitert\`.

## Optional: Belegung

Arbeiten mehrere Sitzungen am selben Projekt, verhindert eine Belegung Kollisionen: Wer in einem Projekt arbeitet,
traegt sich vorher ein und am Ende nur sich selbst wieder aus. Zwei Eintraege desselben Projekts vertragen sich nur,
wenn beide `lesen` sind; sonst wartet der spaetere. Verwaiste Eintraege loescht niemand ausser dem Nutzer. Das Muster ist
freiwillig. Aufbau, Zeile im Auftragskopf und Ablauf: `anleitungen\belegung.md`. Setzt ihr sie nicht ein, steht im
Kopf `Belegung: keine (<Grund>)` oder die Zeile entfaellt.

## Erlaubnisregeln

Im nicht-interaktiven Lauf fragt Claude Code nicht nach; was nicht erlaubt ist, wird abgelehnt. Welche Befehle und
Ordner ein Lauf nutzen darf, steht in den Berechtigungen der Claude-Code-Einstellungen. Das ist eine
Sicherheitseinstellung des Nutzers: Er entscheidet und traegt sie selbst ein. Dieses Paket liefert keine mit. Der
Orchestrator und Claude Code ordnen sie nicht von sich aus um und umgehen eine Ablehnung nicht. Wird etwas abgelehnt,
haelt der Lauf an und nennt den Wortlaut der Ablehnung im Bericht.

## Nachsehen und Anhalten

- Ueberblick: eine Statusdatei, die das Programm bei jedem Lauf schreibt (laufende und wartende Auftraege, seit wann),
  falls der Nutzer sie eingerichtet hat.
- Anhalten: Eine Pausen-Datei (global oder je Strang bzw. Projekt, wie in der Anleitung beschrieben) haelt neue Starts
  an; laufende Auftraege laufen zu Ende. Anlegen und Entfernen ist Sache des Nutzers. Nie ein Fenster schliessen oder
  einen Prozess nach Namen beenden. Liegt ein Auftrag von dir lange in `bereit\`, schau nach, ob eine Pause liegt, und
  sag es dem Nutzer.
