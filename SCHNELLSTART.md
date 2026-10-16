# Schnellstart: in zehn Schritten zum ersten Auftrag

Etwa zehn Minuten. Jeder Schritt hat einen **Kontrollsatz**: Stimmt er nicht, geh nicht weiter. Hintergrund: [README.md](README.md).
Platzhalter: `<Berichte-Ordner>` (dein gemeinsamer Ordner), `<Kuerzel>` (kurzer Name deines Strangs).

1. **Claude Code und Python pruefen.** `claude --version` und `python --version` (unter Linux/macOS `python3`).
   Kontrolle: Beide Befehle geben eine Versionsnummer aus, Python beginnt mit 3.
2. **Paket installieren** (schreibt in deine Nutzereinstellungen, mach es selbst):
   `claude plugin marketplace add dimensionwithin/orchestrator-starter`, dann `claude plugin install orchestrator-starter@orchestrator-starter-marketplace`.
   Kontrolle: `claude plugin list` nennt `orchestrator-starter`.
3. **Berichte-Ordner anlegen** und als Plugin-Einstellung `berichte_ordner` eintragen.
   Kontrolle: Der Ordner existiert und gehoert nur dir.
4. **Unterordner anlegen:** `auftraege`, `post`, `archiv` im `<Berichte-Ordner>`.
   Kontrolle: Alle drei Ordner sind beim Auflisten zu sehen.
5. **Skripte kopieren:** Ordner `setup-post` im `<Berichte-Ordner>` anlegen, `scripts/post-neu.py` und `scripts/marker.py`
   unveraendert hineinkopieren (aus dem Plugin-Ordner, nie direkt dort ausfuehren).
   Kontrolle: `<Berichte-Ordner>/setup-post/` enthaelt beide Dateien.
6. **Orchestrator-Chat starten:** neuer Chat, Skill `orchestrator-starter` aufrufen, `<Kuerzel>` nennen (z. B. `demo`).
   Kontrolle: Der Chat nennt dein Kuerzel und fragt, falls noetig, einmal nach dem Berichte-Ordner.
7. **Ziel beschreiben,** in zwei, drei Saetzen, und um einen kleinen ersten Auftrag bitten.
   Kontrolle: Der Chat schlaegt Modell und Effort mit Begruendung vor und legt `auftraege/<Kennung>.md` an.
8. **Auftrag pruefen:** Letzte Zeile der Datei lesen.
   Kontrolle: Sie lautet `ENDE AUFTRAG <Kennung>`.
9. **Auftrag ausfuehren:** neue Claude-Code-Sitzung im Arbeitsordner, Text:
   `Auftrag <Kennung>: lies <Berichte-Ordner>/auftraege/<Kennung>.md und fuehre ihn aus.` (Modell und Effort wie im Kopf.)
   Kontrolle: Es entsteht `<Berichte-Ordner>/<Kennung>-bericht.md` mit `## Kurzfassung` oben.
10. **Bericht pruefen lassen:** im Orchestrator-Chat "<Kennung> fertig" schreiben.
    Kontrolle: Der Chat liest zuerst nur die Kurzfassung, prueft sie gegen den Auftrag und fuehrt die Uebergabe
    `UEBERGABE-<Kuerzel>.md` nach.

Danach: weitere Auftraege; bei mehreren Chats Post (`post-neu.py`), bei Bedarf eine Warteschlange
([Anleitung](anleitungen/warteschlange-einrichten.md)) und ein Leitstand weiter mit den Anleitungen [Belegung](anleitungen/belegung.md), [Leitstand](anleitungen/leitstand.md) und [Unbeaufsichtigt arbeiten](anleitungen/unbeaufsichtigt.md).
Ein durchgespieltes Beispiel: [beispiele/demo-durchlauf.md](beispiele/demo-durchlauf.md).
