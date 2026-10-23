# Beispiel: ein Durchlauf im erfundenen Strang `demo`

Alles hier ist erfunden. Ordner: `<Berichte-Ordner>`, Kuerzel: `demo`.

## 1. Chat-Start
Du oeffnest einen neuen Chat und rufst den Skill `orchestrator-starter` auf. Du schreibst:
"Strang demo: Ich will ein kleines Rechenskript `rechner.py` mit Tests."
Der Orchestrator antwortet mit Rolle, Kuerzel `demo` und einem Plan in zwei Auftraegen (`demo-1` Skript, `demo-2` Doku).
Er endet mit "Deine Schritte".

## 2. Auftrag (`auftraege/demo-1.md`, gekuerzt)
    Auftrag demo-1 — Rechenskript. AENDERND, mit Commit.
    MODELL: <Modell>      EFFORT: medium      ZEITSPERRE: keine
    ORCHESTRATOR: demo
    Belegung: keine (Uebung, ein einziger Nutzer)
    DEPLOY: kein Deploy

    WARUM: Kleines Skript als Uebung.
    REPO-ZUGRIFF: SCHREIBEND nur <Arbeitsordner>/rechner.py und <Arbeitsordner>/test_rechner.py. Alles andere KEIN ZUGRIFF.
    WAS GETAN WIRD: 1. rechner.py mit add und sub. 2. Zwei Tests, vorher rot. 3. Tests ausfuehren.
    BERICHT: <Berichte-Ordner>/demo-1-bericht.md, oben Kurzfassung.
    ENDE AUFTRAG demo-1

Pruefung durch den Orchestrator: `tail -1 auftraege/demo-1.md` (Windows PowerShell: `Get-Content auftraege\demo-1.md -Tail 1`)
zeigt `ENDE AUFTRAG demo-1`.

## 3. Bericht (`demo-1-bericht.md`, gekuerzt)
    # demo-1 Bericht
    ## Kurzfassung
    Ergebnis: fertig, 2 Tests gruen.
    EINSPRUCH: keiner
    OFFEN FUER DEN NUTZER: nichts
    Modell: <Modell> / medium — passte
    Suite: test_rechner.py 2 passed (GEMESSEN)
    Push: nein
    Deploy: nein
    Belegung: keine

Der Orchestrator liest nur diese Kurzfassung, vergleicht sie mit WAS GETAN WIRD und prueft stichprobenartig, ob GEMESSEN
eine Ausgabe nennt.

## 4. Uebergabe (`UEBERGABE-demo.md`, gekuerzt)
    1. Wer du bist: Strang demo, Kuerzel demo, Arbeitsordner <Arbeitsordner>.
    2. Laufend: nichts.
    3. Offen: 1. demo-2 Doku schreiben lassen.
    4. Entschieden: <Datum> "Nur Addition und Subtraktion."

Nach etwa zehn Antworten schreibt der Orchestrator sie fort, sagt "Dieser Chat ist voll genug, wir wechseln", und du startest
einen neuen Chat, der zuerst nur diesen Kern liest.

## 5. Marker
Nach der Pruefung setzt der Orchestrator den Marker (Skript einmal nach `<Berichte-Ordner>/setup-post/` kopiert):

    python <Berichte-Ordner>/setup-post/marker.py demo "demo-2 freigeben?"

Das Skript legt `leitstand/wartet-demo.txt` an (Zeile 1 Datum und Uhrzeit, Zeile 2 Kurztext). Ist nichts mehr offen:

    python <Berichte-Ordner>/setup-post/marker.py demo --keine

Die Uhrzeit setzt das Skript, nie von Hand.
