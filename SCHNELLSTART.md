# Schnellstart: in zehn Schritten zum ersten Auftrag

Etwa zehn Minuten, ohne die Wartezeit der Chats. Jeder Schritt hat einen **Kontrollsatz**: Stimmt er nicht, geh nicht weiter.
Voraussetzungen und Hintergrund: [README.md](README.md).
Platzhalter: `<Berichte-Ordner>` (dein gemeinsamer Ordner), `<Kuerzel>` (kurzer Name deines Strangs).

1. **Claude Code und Python pruefen.** `claude --version` und `python --version` (unter Linux/macOS `python3`).
   Kontrolle: Beide Befehle geben eine Versionsnummer aus, Python beginnt mit 3.
2. **Paket installieren** (braucht Internet und `git`, schreibt in deine Nutzereinstellungen, mach es selbst):
   `claude plugin marketplace add dimensionwithin/orchestrator-starter`, dann `claude plugin install orchestrator-starter@orchestrator-starter-marketplace`.
   Kontrolle: `claude plugin list` nennt `orchestrator-starter`.
3. **Berichte-Ordner anlegen** und als Plugin-Einstellung `berichte_ordner` eintragen: in Claude Code
   `/plugin configure orchestrator-starter@orchestrator-starter-marketplace` eingeben, den Ordner angeben, danach Claude Code
   neu starten (die Einstellung gilt erst nach dem Neustart).
   Kontrolle: Der Ordner existiert, und im Terminal `claude plugin configure orchestrator-starter@orchestrator-starter-marketplace`
   fuehrt `berichte_ordner` als gesetzt (`set`) auf.
4. **Unterordner anlegen:** `auftraege`, `post`, `archiv` im `<Berichte-Ordner>`.
   Kontrolle: Alle drei Ordner sind beim Auflisten zu sehen.
5. **Skripte kopieren:** Ordner `setup-post` im `<Berichte-Ordner>` anlegen, `scripts/post-neu.py` und `scripts/marker.py`
   unveraendert hineinkopieren, nie direkt aus dem Plugin-Ordner ausfuehren. Quelle: der Plugin-Ordner, bei dir unter
   `<Claude-Konfigordner>\plugins\cache\orchestrator-starter-marketplace\orchestrator-starter\<Version>\scripts\`
   (`<Claude-Konfigordner>` ist meist `.claude` in deinem Benutzerordner; der Pfad ist nur in einer isolierten
   Konfiguration nachgemessen). Die Versionsnummer steht im Pfad und aendert sich bei einem Update. Alternativ lade die
   beiden Dateien aus dem Ordner `scripts` des Repositories `https://github.com/dimensionwithin/orchestrator-starter` herunter.
   Kontrolle: `<Berichte-Ordner>/setup-post/` enthaelt beide Dateien.
6. **Orchestrator-Chat starten:** neue Claude-Code-Sitzung (nicht die, in der spaeter Auftraege laufen), Skill aufrufen,
   `<Kuerzel>` nennen (z. B. `demo`). Der Skill heisst `orchestrator-starter` im Plugin `orchestrator-starter`; die Form
   `/orchestrator-starter:orchestrator-starter` folgt dem Schema `<Plugin>:<Skill>` und ist noch nicht ausprobiert. Ob
   ein Chat ausserhalb von Claude Code den Skill nutzen kann, ist ebenfalls noch nicht ausprobiert. Liegt der Berichte-Ordner
   ausserhalb des Arbeitsordners der Sitzung, gib ihn frei, zum Beispiel mit `claude --add-dir <Berichte-Ordner>`
   (der Schalter steht in `claude --help`, das Zusammenspiel mit dem Skill ist noch nicht ausprobiert).
   Kontrolle: Der Chat nennt dein Kuerzel und fragt, falls noetig, einmal nach dem Berichte-Ordner.
7. **Ziel beschreiben,** in zwei, drei Saetzen, und um einen kleinen ersten Auftrag bitten.
   Kontrolle: Der Chat schlaegt Modell und Effort mit Begruendung vor und legt `auftraege/<Kennung>.md` an
   (mit Warteschlange: `auftraege/bereit/<Kennung>.md`). Willst du den Ablauf erst ohne Chat sehen, kopiere
   `vorlagen/BEISPIEL-AUFTRAG.md` dorthin und fuell die Platzhalter.
8. **Auftrag pruefen:** Letzte Zeile der Datei lesen.
   Kontrolle: Sie lautet `ENDE AUFTRAG <Kennung>`.
9. **Auftrag ausfuehren:** neue Claude-Code-Sitzung im Arbeitsordner, Text:
   `Auftrag <Kennung>: lies <Berichte-Ordner>/auftraege/<Kennung>.md und fuehre ihn aus.` (Modell und Effort wie im Kopf.)
   Der Auftrag schreibt in den Berichte-Ordner: lege ihn im Arbeitsordner an oder gib ihn mit `--add-dir` frei. Ob Claude
   Code beim Schreiben ausserhalb des Arbeitsordners nachfragt oder ablehnt, ist noch nicht ausprobiert.
   Kontrolle: Es entsteht `<Berichte-Ordner>/<Kennung>-bericht.md` mit `## Kurzfassung` oben.
10. **Bericht pruefen lassen:** im Orchestrator-Chat "<Kennung> fertig" schreiben.
    Kontrolle: Der Chat liest zuerst nur die Kurzfassung, prueft sie gegen den Auftrag und fuehrt die Uebergabe
    `UEBERGABE-<Kuerzel>.md` nach.

Danach: weitere Auftraege; bei mehreren Chats Post (`post-neu.py`), bei Bedarf eine Warteschlange
([Anleitung](anleitungen/warteschlange-einrichten.md)) und ein Leitstand weiter mit den Anleitungen [Belegung](anleitungen/belegung.md), [Leitstand](anleitungen/leitstand.md) und [Unbeaufsichtigt arbeiten](anleitungen/unbeaufsichtigt.md).
Ein durchgespieltes Beispiel: [beispiele/demo-durchlauf.md](beispiele/demo-durchlauf.md).

## Tests (optional)

In einem Klon des Repositories (`git clone https://github.com/dimensionwithin/orchestrator-starter`):

- Skripte: im Ordner `scripts/` `python -m unittest` (Linux/macOS `python3`). Kontrolle: `Ran 2 tests` und `OK`.
- Manifest: `claude plugin validate <Ordner-des-Klons>`. Kontrolle: `Validation passed`.
- Waechter-Mod: `claude plugin test <Ordner-des-Klons>`. Kontrolle: `6 pass, 0 fail`.
