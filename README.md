# orchestrator-starter

Ein Starterpaket fuer Claude Code, mit dem du Arbeit auf mehrere Chats verteilst: Ein oder mehrere **Orchestrator-Chats**
planen und schreiben Auftraege als Dateien, **ein Ausfuehrer** (Claude Code) arbeitet sie ab und schreibt Berichte.
Optional gibt es eine **Warteschlange**, die fertige Auftraege selbst startet, **Post** zwischen den Orchestratoren und einen
**Leitstand**, der zeigt, welcher Chat gerade auf dich wartet.

Version 0.2.2. Nichts davon ist veroeffentlicht. Autor `DimensionWithin`, Lizenz MIT (siehe LICENSE).

## Fuer wen

Fuer Leute, die schon mit Claude Code arbeiten und bei groesseren Vorhaben den Faden verlieren: lange Chats werden teuer
und unuebersichtlich, Entscheidungen gehen unter. Das Paket gibt eine feste Aufteilung (Nutzer entscheidet, Orchestrator
plant und prueft, Claude Code fuehrt aus) und feste Dateien fuer alles, was zwischen den Rollen ausgetauscht wird.

## Was enthalten ist

| Teil | Ort im Paket | Zweck |
|---|---|---|
| Skill `orchestrator-starter` | `skills/orchestrator-starter/SKILL.md` | Rolle des Orchestrators, Auftragsaufbau, Modell-Routing, Berichte pruefen, Uebergabe |
| Regeln zum Skill | `skills/orchestrator-starter/regeln/` | `warteschlange.md`, `uebergabe.md`, `unbeaufsichtigt.md` |
| Waechter-Mod | `hooks/` | zeigt die Lauflaenge einer Sitzung an und erinnert an den Abschluss; verbietet nichts |
| Skripte | `scripts/` | `post-neu.py` (neue Post an dein Fenster), `marker.py` ("wartet auf dich"-Marker), `test_marker.py`, `LIESMICH.md` |
| Vorlagen | `vorlagen/` | `BEISPIEL-AUFTRAG.md`, `parallel.txt`, `repos-liste.txt`, `wartet-KUERZEL.txt` |
| Anleitungen | `anleitungen/` | [Warteschlange einrichten](anleitungen/warteschlange-einrichten.md), [Belegung](anleitungen/belegung.md), [Leitstand](anleitungen/leitstand.md), [Unbeaufsichtigt arbeiten](anleitungen/unbeaufsichtigt.md) |
| Schnellstart | [SCHNELLSTART.md](SCHNELLSTART.md) | in zehn Schritten bis zum ersten Auftrag |
| Beispiel | [beispiele/demo-durchlauf.md](beispiele/demo-durchlauf.md) | ein durchgespielter Strang `demo` |

Zu `unbeaufsichtigt` gehoert zusaetzlich die Regel unter `skills/orchestrator-starter/regeln/unbeaufsichtigt.md`.

## Was NICHT enthalten ist

- **Deploy:** keine Deploy-Regeln und keine Deploy-Skripte. Veroeffentlichen entscheidest immer du.
- **Erlaubnisregeln:** keine Rechte-Eintraege und kein Skript, das in deine Einstellungen schreibt. Ob Auto-Modus oder
  Warteschlange etwas ausfuehren duerfen, stellst du selbst ein.
- **Rechtstexte:** keine Datenschutz-, Impressum- oder Lizenztexte fuer deine Projekte.
- **Die Warteschlange selbst:** die Anleitung beschreibt, wie du sie baust; ein fertiges Programm liegt nicht bei.

## Voraussetzungen

- Claude Code (getestet mit 2.1.289; eine untere Grenze ist nicht bekannt).
- Python 3 fuer `post-neu.py` und `marker.py` (nur Standardbibliothek).
- Optional PowerShell 7 (`pwsh`), falls du die Belegung oder die Windows-Aufgabenplanung benutzt.
- Teile der Warteschlange und der Aufgabenplanung sind **nur auf Windows** beschrieben; fuer Linux und macOS gibt die
  Anleitung die Alternative (cron, launchd). Skill, Post-Skript, Marker und Waechter laufen ueberall, wo Claude Code und
  Python laufen.

## Installation (nur dokumentiert)

Die Installation schreibt in deine Nutzereinstellungen. Fuehre sie selbst aus, wenn du das Paket haben willst:

    claude plugin marketplace add dimensionwithin/orchestrator-starter
    claude plugin install orchestrator-starter@orchestrator-starter-marketplace

Den Berichte-Ordner setzt du als Plugin-Einstellung `berichte_ordner` (Typ Ordner). Weiter mit [SCHNELLSTART.md](SCHNELLSTART.md).

## Sicherheitshinweis

Der Waechter-Mod ist ein Plugin mit Funktions-Hooks und **laeuft mit deinen Nutzerrechten**. Der Quelltext liegt offen unter
`hooks/` (`logic.ts`, `register.ts`, `waechter.test.ts`) und ist kurz; lies ihn vor der Installation. Er zeigt nur Hinweise
an, **sendet nichts** und verbietet nichts. Die Skripte unter `scripts/` sind ebenfalls lesbar und nutzen
nur die Python-Standardbibliothek. Schreibe nie Schluessel, Tokens oder Passwoerter in Auftraege, Berichte oder Post.

## Lizenz

MIT (siehe LICENSE).

## Support

Issues im Repository sind erwuenscht (Fehler, Fragen, Verbesserungsvorschlaege). Es gibt keine Zusage zu Antwortzeiten.
Die Nutzung erfolgt ohne Gewaehr, wie in der Lizenz beschrieben.

## Zeitzone

Die Zeitzone Berlin ist fest in `scripts/post-neu.py` eingebaut: Die Funktion `berlin_jetzt()` (Zeile 38 bis 51) liefert die
Ortszeit, in ihr steht `ZoneInfo("Europe/Berlin")` (Zeile 44). Wer eine andere Zeitzone braucht, aendert diese eine Zeile.
Die Rueckfallregel `berlin_regel()` (Zeile 28) gilt nur, falls `zoneinfo` fehlt, und muesste dann ebenfalls angepasst werden.

## Offen

- Autor und Konto sind als Handle eingesetzt; vor einer Weitergabe nach Wunsch aendern.
- Geheimnis-Pruefung: Geprueft am 16.10.2026.
