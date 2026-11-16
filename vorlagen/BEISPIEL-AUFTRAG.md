Auftrag probe-1 — Probeauftrag fuer die Warteschlange: eine Datei anlegen und berichten
MODELL: <Modellname laut deinem Programm>      EFFORT: <low|medium|high|xhigh|max>      ZEITSPERRE: <Zeitfenster, in dem er nicht laufen darf, oder: keine>
ORCHESTRATOR: <Kuerzel>
Belegung: keine (Probe, schreibt nur im Berichte-Ordner)
DEPLOY: kein Deploy
Grundregeln: <Berichte-Ordner>\regeln\grundregeln-auftraege.md gelten

So benutzt du die Vorlage: Kopie nach `<Berichte-Ordner>\auftraege\<Kennung>.md` (mit Warteschlange: `auftraege\bereit\`), Kennung neu vergeben
(Dateiname und erste Zeile gleich, nur `A-Z a-z 0-9 . _ -`), Platzhalter in `<...>` ersetzen, am Ende die letzte Zeile
pruefen (`tail -1`; Windows PowerShell: `Get-Content <Datei> -Tail 1`). Dieser Absatz darf in der Kopie bleiben oder fallen.
Strang `demo` ist erfunden; nimm dein eigenes Kuerzel. Die Zeile `Grundregeln:` setzt voraus, dass die Datei aus Schritt 5 des
Schnellstarts in `<Berichte-Ordner>\regeln\` liegt; dann gelten Verbote, Shell-Regel und Berichtsformat von dort, und der Auftrag
nennt nur seine Zusaetze.

WARUM
ENDZUSTAND (Sicht des Nutzers): Im Berichte-Ordner liegt `demo\hallo.txt`, und ein Bericht zeigt, dass Warteschlange, Bericht
und Post zusammenarbeiten. Nichts davon beruehrt ein echtes Projekt.

WARUM DIESES MODELL
Stufe 1 der Routing-Tabelle (rein mechanisch: eine Datei schreiben), erwartete Laenge unter 10 Antworten.

ENTSCHIEDEN
- Alles ist entschieden, es gibt keine Rueckfrage. Unklares wird begruendet ausgelegt und im Bericht unter EINSPRUCH gemeldet.

REPO-ZUGRIFF
Schreibend nur: `<Berichte-Ordner>\demo\` (neu). Lesend: nichts. Alles andere KEIN ZUGRIFF. Kein Git, kein Push.

STANDORT
`<Berichte-Ordner>\demo\` existiert noch nicht. Gibt es ihn schon: Inhalt nennen, nichts ueberschreiben, anhalten und melden.

HARTE VERBOTE
Die der Grundregeln, dazu: nichts loeschen, keine Prozesse nach Namen beenden, keine Einstellungen von Claude Code aendern.
Lehnt der Auto-Modus etwas ab: nicht umgehen, den Wortlaut berichten.

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
`<Berichte-Ordner>\probe-1-bericht.md` (bei neuer Kennung: `<Berichte-Ordner>\<Kennung>-bericht.md`). Oben `## Kurzfassung`
(hoechstens 20 Zeilen) mit diesen Zeilen in dieser Reihenfolge: `Ergebnis: fertig | teilweise | angehalten, <ein Satz>`,
`EINSPRUCH:`, `OFFEN FUER DEN NUTZER:` (nur Entscheidungen und Handgriffe, ohne die es nicht weitergeht, sonst `nichts`),
`TEST FUER DEN NUTZER:` (was nur ein Mensch am Geraet sieht, sonst `keiner`), `FUER DEN ORCHESTRATOR:` (alles andere, sonst
`keine`), `Modell: <Modell> / <Effort> — passte | zu schwach (<warum>) | groesser als noetig`, Schlusszeilen
`Suite: entfaellt`, `Push: entfaellt`, `Deploy: nein`, `Belegung: keine`. Jede Aussage ist als GEMESSEN, ABGELESEN
oder ABGELEITET markiert.
ENDE AUFTRAG probe-1
