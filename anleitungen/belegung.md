# Belegung: ein Projekt, ein Schreiber

Die Belegung verhindert, dass zwei Sitzungen gleichzeitig im selben Projekt arbeiten und sich gegenseitig
Aenderungen zerstoeren. Sie ist **freiwillig**: Wer nur ein Projekt hat oder nie zwei Sitzungen gleichzeitig laufen
laesst, braucht sie nicht und schreibt in den Auftragskopf `Belegung: keine (<Grund>)`. Das Plugin bringt nur das
Konzept und eine Vorlage fuer die Projektliste mit, kein fertiges Werkzeug und keine Liste von Projekten.

## Das Konzept in fuenf Saetzen

1. Wer in einem Projekt arbeitet (Ordner mit Code oder Daten, meist ein Git-Repository), traegt sich **vorher** ein
   und am Ende wieder aus. Auch rein lesende Auftraege tragen sich ein (als `lesen`).
2. Der Eintrag ist eine kleine Datei im Ordner `<Berichte-Ordner>\belegung\`. Es gilt: **ein Projekt, ein Schreiber.**
3. Zwei Eintraege desselben Projekts vertragen sich nur, wenn **beide** `lesen` sind. Sonst arbeitet der spaetere nicht.
4. Man loescht nur den **eigenen** Eintrag. Eine fremde Datei fasst niemand an, auch keine liegen gebliebene.
5. Ein Eintrag, dessen geschaetztes Ende (`bis_ca`) mehr als 2 Stunden zurueckliegt, gilt als **verwaist**. Er sperrt das
   Projekt weiter, bis ein Mensch ihn pruefen und entfernen lassen hat. Nie automatisch loeschen: Die Sitzung kann
   noch leben.

Das ist die **Zusage**: eine kurze, schriftliche Vereinbarung aller beteiligten Orchestratoren, die genau diese Regeln
nennt und ihre Fassung. Schreib sie einmal in eine Datei `<Berichte-Ordner>\ZUSAGE-belegung.md` (Zeile 1 mit
Fassungsnummer). Aendert sich eine Regel, steigt die Fassung, und alle Beteiligten stimmen zu. Jeder Orchestrator
liest vor dem Eintragen Zeile 1 und haelt an, wenn die Fassung nicht die ist, die er kennt.

## Voraussetzungen

- Ein Ordner `<Berichte-Ordner>\belegung\` (leer anlegen). Fehlt er, startet nichts mit Projekt: "Pruefung ohne
  Ergebnis" gilt als nicht bestanden.
- Eine Liste der Projekte, `<Berichte-Ordner>\belegung-projekte.txt`, aus der Vorlage `vorlagen\repos-liste.txt`.
  Die Vorlage ist leer; **du** traegst deine Projekte ein (Name und Ordner), sonst niemand.
- Eine Liste der erlaubten Orchestrator-Kuerzel (dieselben wie in der Post) und ein Kuerzel fuer dich selbst, wenn du von
  Hand in einem Projekt arbeitest.
- Ein kleines Werkzeug mit den vier Handgriffen unten. Du kannst es von Claude Code bauen lassen (Python, nur
  Standardbibliothek, plattformunabhaengig) und musst es mit Tests absichern, bevor sich jemand darauf verlaesst.
  Eintraege nie von Hand schreiben, nur ueber das Werkzeug.

## Der Eintrag

Dateiname `<Projektname>__<Kennung>.json` im Ordner `belegung\`. Projektname: nur `a-z 0-9 . _ -`, klein. Kennung:
die Auftrags-ID, nur `A-Z a-z 0-9 . _ -`. Inhalt (JSON, UTF-8):

    {
      "kennung": "<Kennung>",
      "art": "lesen",
      "orchestrator": "<Kuerzel>",
      "bis_ca": "<Zeitstempel mit Zeitzone, z. B. 2030-01-02T03:04:05+01:00>",
      "worktree": "<optional: Ordner eines Arbeitsbaums>"
    }

- `art`: **lesen** = nur lesen, analysieren, pruefen. **bauen** = Dateien im Projekt aendern, committen, Tests, die
  schreiben. **ausfuehren** = Pipelines, Skripte mit Wirkung, Downloads, Rechenlast. Im Zweifel die strengere Art.
- `bis_ca` mit Zeitzone (sonst ist der Eintrag unlesbar). Realistisch schaetzen (Vorgabe 2 Stunden); wird es laenger,
  nachfuehren.
- Ein zusaetzlicher Arbeitsbaum (git worktree) belegt dasselbe Projekt wie die Haupt-Arbeitskopie.
- Ein Auftrag, der mehrere Projekte anfasst, traegt sich in **alle** ein, oder in keines.

## Die vier Handgriffe (Ablauf)

1. **Nehmen** in drei Schritten: (a) lesen, ob ein unvertraeglicher Eintrag liegt; (b) den eigenen Eintrag **exklusiv**
   anlegen (schlaegt fehl, wenn die Datei existiert); (c) erneut lesen, ob inzwischen ein anderer unvertraeglicher
   Eintrag dazugekommen ist. Wenn ja: den eigenen Eintrag wieder entfernen und anhalten. Erst wenn alle drei Schritte
   durch sind, beginnt die Arbeit. Anhalten heisst: im Projekt nichts tun, nichts in einer Schleife neu versuchen, die
   Meldung wortgetreu berichten. Gruende zum Anhalten: unvertraeglicher Eintrag, verwaister Eintrag, eigene Kennung
   liegt schon, Eintrag unlesbar, Ordner `belegung\` fehlt, festes Zeitfenster.
2. **Nachfuehren:** Vor jedem laengeren Schritt und spaetestens 30 Minuten vor `bis_ca` das Ende neu setzen (Datei
   atomar ersetzen). Fehlt die Datei oder ist der Inhalt nicht mehr der eigene: Arbeit anhalten und melden.
3. **Freigeben:** am Ende **immer**, auch nach Fehler oder Abbruch. Geloescht wird nur eine Datei mit eigener Kennung
   und eigenem Kuerzel. Klappt es nicht (Datei gesperrt): einmal wiederholen, dann mit Pfad melden. Die liegen
   gebliebene Datei sperrt das Projekt, bis sie weg ist.
4. **Nur nachsehen** (`pruefe`): zeigt, ob ein Projekt frei waere, ohne etwas einzutragen. Ein Orchestrator nutzt das,
   bevor er Auftraege verteilt.

Feste Zeitfenster (zum Beispiel ein Backup oder ein Upload zu bestimmter Uhrzeit) kann das Werkzeug zusaetzlich
pruefen; dann nimmt es kein Projekt, dessen Auftrag in das Fenster hineinliefe. Ob du solche Fenster brauchst, ist
deine Sache.

## Die Zeile im Auftragskopf

    Belegung: repo=<Projektname>[,<weiteres>] art=<lesen|bauen|ausfuehren> kennung=<Kennung> orchestrator=<Kuerzel> stunden=<n>

oder `Belegung: keine (<Grund>)`, z. B. wenn der Auftrag nur im Berichte-Ordner schreibt und in keinem Projekt. Im
Bericht steht am Ende eine Zeile: `Belegung: <Projekte> <Art> <Kennung> genommen <Beginn>, freigegeben ja/nein`.

Verbindung zur Warteschlange: Das Programm (siehe `warteschlange-einrichten.md`) liest dieselbe Zeile. Es startet einen
Auftrag erst, wenn alle seine Projekte frei sind, und uebernimmt dann **nicht** das Eintragen: Das tut der Auftrag selbst
als erste Handlung. Beide Seiten pruefen also dieselbe Ordnerstruktur.

## Kontrolle

1. Projektname in `repos-liste.txt` eingetragen, Ordner `belegung\` vorhanden und leer.
2. Zwei Probeaufrufe mit demselben Projekt: `lesen` + `lesen` vertragen sich; `lesen` + `bauen` nicht (zweiter Aufruf
   haelt an und nennt den ersten). Danach beide freigeben; `belegung\` ist wieder leer.
3. Probe "verwaist": einen Eintrag mit `bis_ca` vor mehr als 2 Stunden von Hand in einem Wegwerf-Berichte-Ordner (nicht
   in deinem echten) anlegen: `nimm` muss anhalten und nichts loeschen.

## Rueckgaengig

Die Belegung zu beenden ist ein Entscheid des Nutzers: Er traegt in den Auftraegen `Belegung: keine (<Grund>)` ein oder
entfernt das Werkzeug. Der Ordner `belegung\` und die Liste duerfen bleiben; liegt dort noch ein Eintrag, prueft ein
Mensch, ob die Sitzung noch lebt, und entfernt ihn dann selbst. Orchestratoren und Laeufe loeschen keine fremden
Eintraege.
