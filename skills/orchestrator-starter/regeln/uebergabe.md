# Regel Uebergabe und Chatwechsel (zum Skill orchestrator-starter)

**Datei:** `<BERICHTE>\UEBERGABE-<Kuerzel>.md`, je Strang genau eine, immer die neueste Fassung. Vorher die bisherige
nach `<BERICHTE>\archiv\UEBERGABE-<Kuerzel>-<JJJJ-MM-TT-HHMM>.md` kopieren (nichts ueberschreiben). Nach dem
Schreiben mit `grep` oder `sha256sum` pruefen. Regeln aus Skills, Vereinbarungen und Regelwerken nur mit Pfad und
Fassung nennen, nicht abschreiben. Keine Schluessel, Tokens oder Passwoerter in die Uebergabe.

Die Uebergabe hat zwei Teile. Kern `UEBERGABE-<Kuerzel>.md`, hoechstens etwa 5 KB (Punkte 1 bis 4 unten). Anhang
`UEBERGABE-<Kuerzel>-anhang.md` fuer die Punkte 5 und 6, "Was gilt" und aeltere Entscheidungen; nur bei Bedarf lesen.

**Anhang hoechstens 40 KB.** Ist er groesser, lagerst du beim naechsten Nachfuehren aus: Entschiedenes, das aelter als 14 Tage
ist, und erledigte Stolpersteine kommen nach `<BERICHTE>\archiv\UEBERGABE-<Kuerzel>-anhang-<JJJJ-MM-TT>.md` (neue Datei; gibt
es den Tag schon, `-HHMM` anhaengen; nichts ueberschreiben, nichts loeschen). Im Anhang bleibt davon nur der Pfad dieser
Datei. Was noch gilt und juenger ist, bleibt im Anhang.

**Aufbau:**
1. Wer du bist: Strang, Kuerzel, Repositories, Ordner, strangeigene Regeln (Pfad, Fassung). Dazu die Zeile
   `Ergebnis statt Stueckelung: regeln\ergebnis-statt-stueckelung.md gilt (ENDZUSTAND in jedem Auftrag, ein Auftrag bis zum
   nutzbaren Ergebnis).`
2. Laufend: Auftraege (Kennung, Ziel, seit wann, was als Naechstes geprueft wird).
3. Offen: nummeriert, das Naechste zuerst; besprochene, nicht entschiedene Fragen gehoeren dazu.
4. Entschieden: Entscheidungen des Nutzers der letzten Tage woertlich mit Datum (aeltere nur mit Verweis); dazu deine
   umgesetzten Empfehlungen, als solche gekennzeichnet.
5. Wichtige Dateien: Berichte, Plaene, Freigaben mit Pfad.
6. Stolpersteine, auch Lehren aus der Modell-Zeile der Berichte (zu schwach / groesser als noetig).

**Wann nachfuehren:** sobald du einen Bericht geprueft hast oder der Nutzer etwas entschieden hat, und immer, wenn er
Feierabend macht oder weg ist. Erledigtes faellt aus dem Kern heraus.

Post liest jeder Chat (falls Post eingesetzt wird) mit `post-neu.py <Kuerzel>` (siehe SKILL.md); das Skript fuehrt die
Lesemarke, nicht die Uebergabe. Gelesen wird nur im neuen Chat, beim Wort "Post" und wenn ein Ergebnis erwartet wird; in
allen anderen Antworten nur `post-neu.py <Kuerzel> --zaehlen` (nennt die Zahl, Lesemarke unveraendert). Post-Eintraege:
ein Eintrag je Thema, Fragen gesammelt am Ende.

**Wann wechseln:** im Fenster Antwort 10 bis 15 (SKILL.md, "Uebergabe und Chatwechsel"); ab Antwort 10 Kern und Anhang
nachfuehren, ab Antwort 15 keine neue Arbeit mehr, nur noch die Wechsel-Antwort.
Zugriff auf `<BERICHTE>`: Fehlt er im neuen Chat, gilt der Abschnitt "Der Berichte-Ordner" der SKILL.md; bis er
freigegeben ist, liest oder schreibt der Chat nichts auf dem Rechner.

**Die Wechsel-Antwort:**
- Uebergabe fertig schreiben und pruefen.
- Ein Satz: "Dieser Chat ist voll genug, wir wechseln. Die Uebergabe liegt in `<BERICHTE>\UEBERGABE-<Kuerzel>.md`."
- Deine Schritte: 1. Einen neuen Chat oeffnen (am besten im selben Projekt bzw. Arbeitsordner). 2. Einfuegen
  (Codeblock, fester Startsatz, mit eingesetztem Pfad):
  `Du bist Orchestrator <Kuerzel>. Lade den Skill orchestrator-starter. Lies <BERICHTE>\UEBERGABE-<Kuerzel>.md und
  arbeite unter "Offen" weiter.` 3. Den alten Chat nicht mehr benutzen.
- Mit Leitstand: der neue Chat setzt als Erstes `marker.py <Kuerzel> --keine` oder den echten Stand und schreibt seine
  Chat-Adresse neu (SKILL.md, Abschnitt "Leitstand und Marker").
- Der neue Chat liest zuerst nur den Kern, ruft `post-neu.py <Kuerzel>` auf (falls Post eingesetzt wird), dann die
  Berichte zu "Laufend" (je zuerst `head -25`). Anhang und alte Berichte nur bei Bedarf.
