# Regel: Ergebnis statt Stueckelung (zum Skill orchestrator-starter)

Anlass: Systeme werden leicht in zu viele kleine Zwischenschritte zerlegt. Beispiel: Eine neue Fassung einer Vereinbarung
brauchte einen Auftrag fuer die Vereinbarung, einen, der anhielt, einen fuer den Skill, einen fuer das Startprogramm und eine
Rundnachricht; in der Zwischenzeit liefen andere Auftraege ohne Arbeit. Die Grenze "hoechstens etwa 150 Antworten" ist eine
Obergrenze, kein Richtwert: die meisten Auftraege dauern 10 bis 40 Antworten.

## 1 Ziel zuerst
Jeder Auftrag nennt in WARUM den **ENDZUSTAND** aus Sicht des Nutzers: was funktioniert, wenn der Auftrag fertig ist
("alle Chats koennen die neue Fassung benutzen"), nicht nur die Arbeit ("Skill anpassen").

## 2 Ein Auftrag bis zum nutzbaren Ergebnis
Zusammen in einen Auftrag gehoert, was zusammen erst nuetzt: Aenderung, Tests, Doku, Umstellung der abhaengigen Stellen
(Skill, Startprogramm, Regeldateien, Hinweis-Text) und, wo erlaubt, der Weg bis zum Einsatz. Nie trennen, wenn der
Zwischenstand Schaden anrichtet oder ohne den Rest nichts nuetzt (Regelwechsel und Folgeauftrag im selben Zug).

## 3 Selbsttest vor dem Schneiden
"Wenn nur dieser eine Auftrag fertig wird und nichts weiter kommt: ist der Nutzer besser dran?" Nein: zusammenlegen.

## 4 Aufteilen nur, wenn
- mehr als etwa 100 Antworten zu erwarten sind, oder
- die Teile unabhaengig pruefbar UND jeder fuer sich nuetzlich ist, oder
- verschiedene Projekte betroffen sind, die sich nicht vertragen (Belegung), oder
- dazwischen ein ausdrueckliches Ja des Nutzers noetig ist (Geld, Konten, Loeschen, Veroeffentlichen, Rechtstexte,
  Vereinbarungen, Sicherheit).
Mess-, Probe- und Bestandsaufnahme-Auftraege nur, wenn aus ihrem Ergebnis eine echte Entscheidung folgt; sonst die
Messung als ersten Schritt im Bauauftrag.
Wird wegen "mehr als etwa 100 Antworten" geteilt und ist der Weg offen, kommt zuerst ein Plan-Auftrag
(`regeln\plan-auftrag.md`); die Teile stehen dann im Plan, jeder mit eigenem Endzustand und eigener Pruefung, und werden
als Stufe 2 gebaut.

## 5 Anspruch im Auftrag
In WAS GETAN WIRD ein Satz: "Ziel ist das bestmoegliche nutzbare Ergebnis, nicht das Abhaken der Liste." Im EINSPRUCH darf
Claude Code Luecken schliessen, die der Auftrag uebersehen hat, solange es im REPO-ZUGRIFF und in den HARTEN VERBOTEN
bleibt; was in diesem Auftrag in etwa einer Stunde machbar ist, wird nicht auf einen Folgeauftrag geschoben. Berichte nennen
unter FUER DEN ORCHESTRATOR nur Luecken, die wirklich ausserhalb des Rahmens liegen.

## 6 Pruefen
Der Orchestrator zaehlt beim Planen die Auftraege je Ziel. Mehr als zwei fuer dasselbe Ziel: stehen bleiben und fragen,
ob ein Auftrag reicht.

## 7 Lauflaenge: eine Regel
- **Planwert:** die meisten Auftraege dauern 10 bis 40 Antworten; wer mehr als etwa 100 Antworten erwartet, teilt (Abschnitt 4).
- **Obergrenze 150 Antworten** (SKILL.md, "Auftraege schneiden"). Der mitgelieferte Waechter-Mod (`hooks\logic.ts`) weist
  bei 100 hin und erinnert ab 150 an den Abschluss. Bei dem Hinweis sichert der Lauf seinen Zwischenstand und schliesst ab.
- **Strangwerte** in einer Uebergabe (z. B. "hoechstens 40 bis 45 planen") sind **Strangregeln**: sie gelten nur fuer den
  Strang, der sie in seiner Uebergabe nennt, gehen dort vor und aendern die Obergrenze 150 nicht.
