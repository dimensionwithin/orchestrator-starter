# Beispiel: ein Durchlauf im erfundenen Strang `demo`

Alles hier ist erfunden. Ordner: `<Berichte-Ordner>`, Kuerzel: `demo`.

## 1. Chat-Start
Du oeffnest einen neuen Chat und rufst den Skill `orchestrator-starter` auf. Du schreibst:
"Strang demo: Ich will ein kleines Rechenskript `rechner.py` mit Tests."
Der Orchestrator antwortet mit Rolle, Kuerzel `demo` und einem Plan in zwei Auftraegen (`D-1` Skript, `D-2` Doku).
Er endet mit "Deine Schritte".

## 2. Auftrag (`auftraege/D-1.md`, gekuerzt)
    Auftrag D-1 — Rechenskript. AENDERND, mit Commit.
    MODELL: <Modell>      EFFORT: medium      ZEITSPERRE: keine
    ORCHESTRATOR: demo
    Belegung: keine (Uebung, ein einziger Nutzer)
    DEPLOY: kein Deploy

    WARUM: Kleines Skript als Uebung.
    REPO-ZUGRIFF: SCHREIBEND nur <Arbeitsordner>/rechner.py und <Arbeitsordner>/test_rechner.py. Alles andere KEIN ZUGRIFF.
    WAS GETAN WIRD: 1. rechner.py mit add und sub. 2. Zwei Tests, vorher rot. 3. Tests ausfuehren.
    BERICHT: <Berichte-Ordner>/D-1-bericht.md, oben Kurzfassung.
    ENDE AUFTRAG D-1

Pruefung durch den Orchestrator: `tail -1 auftraege/D-1.md` zeigt `ENDE AUFTRAG D-1`.

## 3. Bericht (`D-1-bericht.md`, gekuerzt)
    # D-1 Bericht
    ## Kurzfassung
    Ergebnis: fertig, 2 Tests gruen.
    EINSPRUCH: keiner
    OFFEN FUER DEN NUTZER: nichts
    Modell: <Modell> / medium — passte
    Suite: test_rechner.py 2 passed (GEMESSEN)

Der Orchestrator liest nur diese Kurzfassung, vergleicht sie mit WAS GETAN WIRD und prueft stichprobenartig, ob GEMESSEN
eine Ausgabe nennt.

## 4. Uebergabe (`UEBERGABE-demo.md`, gekuerzt)
    1. Wer du bist: Strang demo, Kuerzel demo, Arbeitsordner <Arbeitsordner>.
    2. Laufend: nichts.
    3. Offen: 1. D-2 Doku schreiben lassen.
    4. Entschieden: <Datum> "Nur Addition und Subtraktion."

Nach etwa zehn Antworten schreibt der Orchestrator sie fort, sagt "Dieser Chat ist voll genug, wir wechseln", und du startest
einen neuen Chat, der zuerst nur diesen Kern liest.

## 5. Marker
Nach der Pruefung setzt der Orchestrator den Marker (Skript einmal nach `<Berichte-Ordner>/setup-post/` kopiert):

    python <Berichte-Ordner>/setup-post/marker.py demo "D-2 freigeben?"

Das Skript legt `leitstand/wartet-demo.txt` an (Zeile 1 Uhrzeit, Zeile 2 Kurztext). Ist nichts mehr offen:

    python <Berichte-Ordner>/setup-post/marker.py demo --keine

Die Uhrzeit setzt das Skript, nie von Hand.
