# Regel Plan-Auftrag (zum Skill orchestrator-starter)

Woerter: **Plan-Auftrag** = ein lesender Auftrag, dessen einziges Ergebnis eine Plan-Datei ist. **Bau nach Plan** = ein Auftrag,
der diese Datei Schritt fuer Schritt ausfuehrt. **Antwort** = ein Arbeitsschritt des Modells. Modelle heissen hier wie in der
Routing-Tabelle des Skills: kleines, mittleres, grosses Modell; Stufen wie dort.

## 1 Wann ein Plan-Auftrag lohnt und wann nicht

Er soll drei Dinge sparen:
1. **Das teure Modell beim Bauen.** Mit Plan baut das mittlere Modell / medium (Stufe 2), was sonst das grosse Modell
   (Stufe 3) braucht.
2. **Fehlstarts.** Der Orchestrator sieht das Projekt oft nicht selbst; ein Auftrag nennt dann einen Stand, der nicht mehr
   stimmt. Der Planer liest das Projekt selbst und schreibt den gemessenen Standort in den Plan.
3. **Lange Laeufe.** Eine Antwort kostet in sehr langen Laeufen deutlich mehr als in kurzen. Der Plan schneidet den Bau in
   Teile, die jeder fuer sich nuetzen.

| Lage | Was tun |
|---|---|
| Ein Auftrag, Weg klar, bis etwa 40 Antworten | **kein Plan-Auftrag.** Der Orchestrator schreibt die Schritte in den Auftrag. Stufe 2 |
| Ein Auftrag, Weg klar, aber laenger | kein Plan-Auftrag; Auftrag nach Abschnitt 3 so genau schreiben wie einen Plan. Stufe 2 |
| Ein Auftrag, Weg offen, bis etwa 100 Antworten | kein Plan-Auftrag; das grosse Modell / medium plant und baut in einem (Stufe 3) |
| Bau ueber etwa 100 Antworten oder mehrere Auftraege, Weg offen | **Plan-Auftrag an das staerkste verfuegbare Modell / medium**, danach Bau nach Plan |
| Architektur ueber mehrere Projekte, Fehler nach zwei Versuchen nicht gefunden | **Plan-Auftrag an das staerkste verfuegbare Modell / high** |
| Zwischenstand waere schaedlich, Teile nicht einzeln pruefbar | nicht teilen (`ergebnis-statt-stueckelung.md` Abschnitt 2); ein Auftrag auf Stufe 3 oder 4, Plan hoechstens als erster Schritt im selben Lauf |

Grob gerechnet holt eine Plan-Sitzung ihre Kosten erst bei einem Bau von einigen Dutzend Antworten wieder herein (mit
Effort high erst bei deutlich mehr). Darunter ist der Plan teurer als das, was er spart.

## 2 Der Plan-Auftrag (Kopf wie jeder Auftrag; Besonderheiten)

    Auftrag <Kennung> — Plan fuer <Ziel>. LESEND (Ergebnis: Plan-Datei, kein Commit).
    MODELL: <staerkstes verfuegbares Modell>      EFFORT: medium        (high nur bei Architektur ueber mehrere Projekte)
    Belegung: repo=<name> art=lesen kennung=<Kennung> orchestrator=<Kuerzel> stunden=1
    WARUM: ENDZUSTAND (Sicht des Nutzers). Was soll am Ende funktionieren?
    WARUM DIESES MODELL: Plan, Bau ueber etwa 100 Antworten, Weg offen.
    ENTSCHIEDEN: Wortlaut des Nutzers mit Datum; was schon feststeht, plant der Planer nicht neu.
    REPO-ZUGRIFF: LESEND <Projekt>; SCHREIBEND nur `<BERICHTE>\<Kennung>-dateien\plan.md` (und Hilfsdateien dort).
    WAS GETAN WIRD: 1. Standort messen. 2. Wege vergleichen (hoechstens drei), einen waehlen, die anderen in je einem Satz verwerfen.
      3. Plan nach `regeln\plan-auftrag.md` Abschnitt 3 schreiben. 4. Ohne-Raten-Probe (Abschnitt 4) am eigenen Plan machen und das Ergebnis anhaengen.
    HARTE VERBOTE: nichts im Projekt aendern, keine Auftraege einreihen, nichts bauen "weil es schnell geht".
    PRUEFUNG: Ohne-Raten-Probe bestanden; jede Angabe zum Standort ist GEMESSEN mit Befehl.

Erwartete Groesse: 20 bis 40 Antworten. Der Planer baut nie selbst. Danach baut Stufe 2 nach dem Plan (Kopfzeile `PLAN:`);
Teile, die der Plan als "Urteil noetig" kennzeichnet, baut Stufe 3.

## 3 Aufbau der Plan-Datei (`plan.md`)

1. **Ziel und Endzustand** (drei Saetze, aus Sicht des Nutzers) und **was nicht dazugehoert** (Zaun: Dateien und Themen, die keiner anfasst).
2. **Standort, gemessen:** Zweig, Commit, Zahl der gruenen Tests, Datum und Uhrzeit, der Befehl dazu. Dazu: "Der Bau prueft diese drei Zahlen zuerst;
   weichen sie ab, haelt er an."
3. **Entscheidungen:** was gewaehlt wurde, in je einem Satz warum, und was verworfen wurde. Der Ausfuehrende entscheidet diese Punkte nicht neu.
4. **Teile.** Jedes Teil ist ein Auftrag: eigener Endzustand, eigene Pruefung, fuer sich nuetzlich, hoechstens etwa 60 Antworten. Je Teil:
   - Stufe: "Stufe 2 (nach Plan)" oder ausdruecklich **"Urteil noetig, Stufe 3"** mit dem Grund,
   - Reihenfolge und Abhaengigkeit (`NACH:`), Belegung (Projekt, Art), Schaetzung in Antworten.
5. **Schritte je Teil**, nummeriert. Jeder Schritt nennt:
   - **wo:** Datei mit Pfad, Funktion oder Abschnitt (bei neuen Dateien: Pfad und Zweck),
   - **was:** vorher -> nachher in Worten; bei Schnittstellen der genaue Name, die Parameter und der Rueckgabewert; bei Texten der Wortlaut,
   - **Test:** Name des Tests, was er behauptet, wie er zuerst rot wird, der Befehl und das erwartete Ergebnis (Zahl gruen),
   - **Ende des Schritts:** woran der Ausfuehrende sieht, dass er fertig ist.
6. **Freiraeume, ausdruecklich:** "Hier darf der Ausfuehrende waehlen: ..." (Namen lokaler Variablen, Reihenfolge innerhalb einer Datei) und
   "Hier haelt er an und meldet: ..." (Standort weicht ab, ein genannter Name existiert nicht, ein Test bleibt nach zwei Versuchen rot).
7. **Abnahme des Ganzen:** Befehle mit erwarteter Ausgabe; was der Nutzer am Geraet sehen soll (fuer `TEST FUER DEN NUTZER`).
8. **Risiken und Rueckweg:** was schiefgehen kann, wie man zuruecknimmt (Commit je Teil, `git revert`).
9. **Anhang: Ohne-Raten-Probe** (Abschnitt 4) mit Ergebnis.

Laenge: so kurz wie moeglich, so genau wie noetig. Richtwert 150 bis 400 Zeilen; ein Plan, den der Ausfuehrende nicht ganz liest, ist zu lang.
Code steht nur dort im Plan, wo Worte mehrdeutig waeren (Signaturen, Datenformate, Wortlaut von Meldungen), nicht als fertige Loesung.

## 4 Wie genau ist genau genug? Die Ohne-Raten-Probe

Ein Schritt ist genau genug fuer das mittlere Modell / medium, wenn sich **ohne Blick ins Projekt** fuenf Fragen beantworten lassen:
1. Welche Datei und welche Stelle?
2. Was steht dort nachher anders als vorher?
3. Welcher Test belegt es, und wie heisst er?
4. Welcher Befehl prueft es, mit welchem erwarteten Ergebnis?
5. Was tut der Ausfuehrende, wenn die Stelle anders aussieht als beschrieben?

Dazu eine Wortsuche im Plan. Jedes dieser Woerter in einem Schritt heisst, dass dort noch jemand entscheiden muss: "passend", "geeignet",
"sinnvoll", "bei Bedarf", "gegebenenfalls", "aehnlich wie", "entsprechend", "usw.", "analog", "aufraeumen", "optimieren", "verbessern".
Entweder der Planer entscheidet es jetzt, oder der Schritt (das Teil) wird als **"Urteil noetig, Stufe 3"** gekennzeichnet. Beides ist in
Ordnung; nicht in Ordnung ist ein Schritt, der nach Stufe 2 aussieht und Stufe 3 verlangt.

Der Orchestrator macht die Probe an zwei zufaelligen Schritten nach, bevor er die Bauauftraege schreibt.
