# Regel Unbeaufsichtigt und ueber Nacht (zum Skill orchestrator-starter)

Es kann gearbeitet werden, waehrend der Nutzer schlaeft oder weg ist. Eine Uhrzeit, ab der nichts laufen darf, gibt es
nicht. Grenzen setzen nur feste Zeitfenster, die der Nutzer oder der Strang vereinbart hat (z. B. ein Backup oder ein
Upload zu bestimmter Zeit), und die ZEITSPERRE im Auftrag.

Ist der Nutzer weg (er sagt es, oder es kommt nichts mehr), gilt fuer deine Auftraege:
- **Plane fuer die ganze Zeit.** Mehrere Auftraege nacheinander, oder ein Auftrag mit mehreren entschiedenen Teilen
  ("Nachtpaket"). Ein Teil, der nicht vom vorigen abhaengt, laeuft weiter, auch wenn der vorige scheitert.
- **Nur Entschiedenes.** Nicht getan, sondern im Bericht unter OFFEN FUER DEN NUTZER: Veroeffentlichen, Deploy, Loeschen
  echter Daten, Geld ausserhalb des vereinbarten Rahmens, Sicherheitseinstellungen, eine neue Lesart. Push nur, wenn
  der Auftrag ihn ausdruecklich erlaubt.
- **Sauber anhalten** bei Sicherheitseinstellungen, fremden Prozessen oder Daten, Dateien ausserhalb des Schreibumfangs
  und bei einer Kollision mit anderer Arbeit (z. B. Belegung, falls ihr sie einsetzt): Teil beenden, Belegung
  freigeben, naechster unabhaengiger Teil. Lehnt der Auto-Modus etwas ab: nicht umgehen, den Wortlaut berichten.
- **Zeitangaben realistisch** schaetzen und nie in ein festes Fenster hineinplanen.
- **Riskante echte Laeufe** nur, wenn ein Fehlschlag ohne den Nutzer harmlos bleibt (Abbruch statt Schaden).
- **Keine Rueckfrage** an den Nutzer; Offenes legt Claude Code begruendet aus und meldet es unter EINSPRUCH.
- **Aktiv abwarten:** Startet ein Auftrag etwas im Hintergrund, wartet er darauf und endet erst nach dem Bericht und
  der Freigabe der Belegung; sonst bleibt die Arbeit halb liegen.
- **Bericht:** kurze Zusammenfassung je Teil, OFFEN FUER DEN NUTZER. Ist der Nutzer zurueck, fasst du es in wenigen Zeilen
  zusammen und legst ihm das Offene nummeriert mit deiner Empfehlung vor.
- **Uebergabe nachfuehren**, bevor der Nutzer weggeht, damit ein Chatwechsel in der Zwischenzeit nichts verliert
  (`regeln\uebergabe.md`).
- Vorbedingungen, die der Nutzer fuer den Strang entschieden hat (z. B. "erst ein Probelauf, dann unbeaufsichtigt"),
  bleiben bestehen.
