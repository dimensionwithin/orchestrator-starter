Auftrag demo-1 — Probeauftrag fuer die Warteschlange: eine Datei anlegen und berichten
MODELL: <Modellname laut deinem Programm>      EFFORT: <low|medium|high|xhigh|max>
ORCHESTRATOR: <Kuerzel>
Belegung: keine (Probe, schreibt nur im Berichte-Ordner)
DEPLOY: kein Deploy
ZEITSPERRE: <Zeitfenster, in dem er nicht laufen darf, oder: keine>

So benutzt du die Vorlage: Kopie nach `<Berichte-Ordner>\auftraege\bereit\<Kennung>.md`, Kennung neu vergeben
(Dateiname und erste Zeile gleich, nur `A-Z a-z 0-9 . _ -`), Platzhalter in `<...>` ersetzen, am Ende `tail -1`
pruefen. Dieser Absatz darf in der Kopie bleiben oder fallen. Strang `demo` ist erfunden; nimm dein eigenes Kuerzel.

WARUM
Prueft, dass Warteschlange, Bericht und Post zusammenarbeiten. Nichts davon beruehrt ein echtes Projekt.

ENTSCHIEDEN
- Alles ist entschieden, es gibt keine Rueckfrage. Unklares wird begruendet ausgelegt und im Bericht unter EINSPRUCH gemeldet.

ZUGRIFF
Schreibend nur: `<Berichte-Ordner>\demo\` (neu). Lesend: nichts. Alles andere KEIN ZUGRIFF. Kein Git, kein Push.

STANDORT
`<Berichte-Ordner>\demo\` existiert noch nicht. Gibt es ihn schon: Inhalt nennen, nichts ueberschreiben, anhalten und melden.

HARTE VERBOTE
Nichts loeschen, keine Prozesse nach Namen beenden, keine Einstellungen von Claude Code aendern. Lehnt der Auto-Modus
etwas ab: nicht umgehen, den Wortlaut berichten.

WAS GETAN WIRD
1. Ordner `<Berichte-Ordner>\demo\` anlegen.
2. Darin `hallo.txt` mit dem Inhalt `Probe <Kennung>` und der aktuellen Uhrzeit schreiben (UTF-8).
3. Die Datei zurueckgelesen im Bericht nennen.

PRUEFUNG
Die Datei `hallo.txt` existiert und enthaelt genau die Zeilen aus Schritt 2 (GEMESSEN, mit dem Inhalt belegt).

COMMIT
entfaellt (kein Projekt).

EINSPRUCH
Technisch Unklares begruendet auslegen und melden. ANHALTEN nur bei Zugriff ausserhalb des Schreibumfangs.

BERICHT
`<Berichte-Ordner>\demo-1-bericht.md` (bei neuer Kennung: `<Berichte-Ordner>\<Kennung>-bericht.md`). Oben eine
Kurzfassung (hoechstens 20 Zeilen): Ergebnis, EINSPRUCH, OFFEN FUER DEN NUTZER, eine Zeile
`Modell: <Modell> / <Effort> — passte | zu schwach (<warum>) | groesser als noetig`, Schlusszeilen
`Suite: entfaellt`, `Push: entfaellt`, `Deploy: nein`, `Belegung: keine`. Jede Aussage ist als GEMESSEN, ABGELESEN
oder ABGELEITET markiert.
ENDE AUFTRAG demo-1
