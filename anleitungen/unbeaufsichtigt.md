# Unbeaufsichtigter Betrieb ueber Nacht

Mit Warteschlange kann gearbeitet werden, waehrend du schlaefst oder weg bist. Diese Anleitung sagt, wie du das
einrichtest und kontrollierst. Die Verhaltensregeln der Orchestratoren stehen in `regeln\unbeaufsichtigt.md`; hier
geht es um den Betrieb.

## Voraussetzungen

- Eine laufende Warteschlange nach `warteschlange-einrichten.md`, einschliesslich der Probe (Pause, Scheitern).
- Dein Rechner bleibt an: Energieeinstellungen auf "nie in den Ruhezustand", solange Auftraege laufen. Ein Laptop
  gehoert an Strom und auf eine Unterlage, die die Waerme abfuehrt.
- Du hast die Rechte der Laeufe selbst festgelegt und geprueft (die Anleitung liefert keine). Was nicht erlaubt ist,
  wird abgelehnt; der Lauf haelt an und nennt den Wortlaut im Bericht, statt es zu umgehen.
- Die Auftraege sind **entschieden**: Kein Auftrag in `bereit\` braucht eine Antwort, eine Anmeldung oder einen
  Handgriff von dir.

## Schritte

1. **Fuer die ganze Zeit planen.** Lege mehrere Auftraege nacheinander in `auftraege\bereit\` oder einen Auftrag mit
   mehreren entschiedenen Teilen ("Nachtpaket"). Ein Teil, der nicht vom vorigen abhaengt, laeuft auch dann weiter,
   wenn der vorige scheitert. Jeder Auftrag ist so klein, dass er in der Zeitgrenze deines Programms fertig wird.
2. **Nur Entschiedenes.** Jeder Auftrag nennt im Kopf, was er **nicht** tut. Nicht getan, sondern im Bericht unter
   "OFFEN FUER DEN NUTZER" notiert werden: Veroeffentlichen, Deploy, Loeschen echter Daten, Geld ausserhalb des
   vereinbarten Rahmens, Aenderungen an Sicherheitseinstellungen, eine neue Auslegung. `DEPLOY: kein Deploy` und
   `Push: entfaellt` stehen ausdruecklich im Kopf, wenn du beides nicht willst.
3. **Zeitfenster beachten.** Feste Fenster (Backup, Upload, Wartung) und die ZEITSPERRE im Auftrag kennt die
   Warteschlange nur, wenn du sie eingebaut hast. Reihe nichts ein, das hineinfaellt.
4. **Belegung** (falls ihr sie einsetzt): realistische Stunden im Auftragskopf, ein Auftrag pro Projekt gleichzeitig,
   wenn er schreibt. Bei einer Kollision haelt der Auftrag sauber an, gibt frei und meldet es; der naechste
   unabhaengige Teil laeuft weiter.
5. **Riskante echte Laeufe** nur, wenn ein Fehlschlag ohne dich harmlos bleibt: Abbruch statt Schaden. Was du nicht
   zuruecknehmen kannst, laeuft nicht nachts.
6. **Gleichzeitigkeit begrenzen.** Setze `parallel.txt` auf eine Zahl bis **6**. Aus der Praxis: Sechs Auftraege
   gleichzeitig reichen; darueber wird kaum etwas schneller, aber der Rechner laeuft heiss (Lueftergeraeusch, Drosselung
   von CPU und Grafikkarte), und die Laeufe verbrauchen das Nutzungskontingent deines Abos entsprechend schneller
   (ABGELEITET: mehr Sitzungen, mehr Verbrauch). Fang mit 3 an und erhoehe erst, wenn die Temperatur und die Berichte
   es hergeben.
7. **Aktiv abwarten.** Der Prozess eines Laufs endet, sobald seine Antwort endet. Ein Auftrag, der etwas im Hintergrund
   startet, muss darauf warten (Status wiederholt pruefen) und erst nach dem Bericht und der Freigabe der Belegung
   enden; sonst bleibt Arbeit halb liegen. Schreib das als Satz in den Startauftrag deines Programms.
8. **Uebergabe nachfuehren**, bevor du gehst, damit ein Chatwechsel in der Zwischenzeit nichts verliert
   (`regeln\uebergabe.md`).

## Notbremse

- `auftraege\PAUSE` anlegen: Es startet nichts Neues; Laufende laufen zu Ende. Datei loeschen setzt fort.
- `parallel.txt` auf `1`: hoechstens ein Auftrag gleichzeitig.
- Einen einzelnen Lauf beenden, der wirklich haengt: nur ueber die Prozessnummer aus seiner `.pid`-Datei, nie nach
  Prozessnamen (das trifft fremde Programme), und nur, wenn das Programm ihn nicht selbst per Zeitgrenze beendet.
- Nie ein Fenster schliessen: Das beendet laufende Auftraege unkontrolliert.
- Lehnt der Auto-Modus eine Aktion ab, wird die Ablehnung nicht umgangen, nicht durch andere Befehle, nicht durch
  gelockerte Rechte mitten im Lauf. Sie wird im Bericht wortgetreu gemeldet.

## Kontrolle am Morgen

1. `stand.txt`: Was laeuft noch, was wartet, liegt eine Pause?
2. `auftraege\gescheitert\`: Je Datei die `.grund.txt` lesen. Ursachen wie Rechte, Netz, Zeitsperre oder Belegung
   behebst du an der Ursache; das Modell hochstufen nur, wenn es am Koennen lag.
3. Die Post `post\VON-WARTESCHLANGE.md` und die Kurzfassung (die ersten 20 Zeilen) jedes Berichts: Ergebnis, EINSPRUCH,
   OFFEN FUER DEN NUTZER, Selbsteinschaetzung zum Modell.
4. `belegung\` ist leer (falls ihr sie einsetzt). Eine liegen gebliebene Datei prueft ein Mensch.
5. Das Offene fasst dir der Orchestrator in wenigen Zeilen zusammen, nummeriert, mit Empfehlung.

## Rueckgaengig

Alles, was ein naechtlicher Lauf tut, laesst sich anhalten und nachsehen: Pause anlegen oder die Aufgabe deaktivieren
(`warteschlange-einrichten.md`, "Rueckgaengig"). Bereits fertige Auftraege liegen in `erledigt\` mit Bericht, nichts
wird geloescht. Aenderungen an deinen Projekten machst du ueber deren eigene Versionsverwaltung rueckgaengig (zum
Beispiel mit einem neuen Gegen-Commit), nie mit einem Befehl, der Verlauf zerstoert.
