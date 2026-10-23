# orchestrator-starter

Ein Starterpaket fuer Claude Code, mit dem du Arbeit auf mehrere Chats verteilst: Ein oder mehrere **Orchestrator-Chats**
planen und schreiben Auftraege als Dateien, **ein Ausfuehrer** (Claude Code) arbeitet sie ab und schreibt Berichte.
Optional beschreibt das Paket eine **Warteschlange** (eine Bauanleitung, kein fertiges Programm; sie soll fertige Auftraege
selbst starten), **Post** zwischen den Orchestratoren und einen **Leitstand** (ein Dateiformat, das zeigt, welcher Chat
gerade auf dich wartet; die Anzeige baust du selbst). Was die fett gedruckten Woerter bedeuten, steht unter
[Begriffe](#begriffe).

Version 0.2.5. Autor `DimensionWithin`, Lizenz MIT (siehe LICENSE).

## Fuer wen

Fuer Leute, die schon mit Claude Code arbeiten und bei groesseren Vorhaben den Faden verlieren: lange Chats werden teuer
und unuebersichtlich, Entscheidungen gehen unter. Das Paket gibt eine feste Aufteilung (Nutzer entscheidet, Orchestrator
plant und prueft, Claude Code fuehrt aus) und feste Dateien fuer alles, was zwischen den Rollen ausgetauscht wird.

Sprache: Alle Texte des Pakets sind deutsch (Umlaute als ae, oe, ue geschrieben).

## Begriffe

- **Orchestrator:** ein Claude-Chat, der plant, Auftraege als Dateien schreibt und Berichte prueft, aber selbst nichts an deinen Projekten aendert.
- **Strang:** ein abgegrenztes Arbeitsgebiet (ein Projekt, ein Produkt, ein Thema) mit einem kurzen Kuerzel; jeder Strang hat einen Orchestrator.
- **Berichte-Ordner:** der gemeinsame Ordner auf deinem Rechner, in dem Auftraege, Berichte, Post und Uebergaben liegen; du setzt ihn als Plugin-Einstellung `berichte_ordner`.
- **Auftrag:** eine Textdatei mit Ziel, Zugriffsgrenzen und Pruefung, die Claude Code abarbeitet.
- **Bericht:** die Textdatei, in der Claude Code nach dem Auftrag Ergebnis und Messungen festhaelt, oben mit einer Kurzfassung.
- **Post:** kurze Eintraege in Dateien, mit denen sich Orchestratoren gegenseitig etwas ausrichten, ohne dass du Nachrichten traegst.
- **Leitstand:** eine Uebersicht, welcher Orchestrator auf dich wartet; im Paket nur als Dateiformat beschrieben (siehe [Leitstand](anleitungen/leitstand.md)).
- **Warteschlange:** ein Programm, das fertige Auftraege aus einem Ordner nacheinander startet; im Paket nur als Bauanleitung beschrieben.
- **Belegung:** eine kleine Datei pro Projekt, mit der sich eine Sitzung als Schreiber eintraegt, damit nie zwei gleichzeitig dasselbe Projekt aendern; freiwillig (siehe [Belegung](anleitungen/belegung.md)).
- **Auto-Modus:** eine Betriebsart von Claude Code, in der ein Pruefer statt dir entscheidet, ob eine Aktion erlaubt ist; er lehnt ab, was er nicht freigibt.
- **Mod / Funktions-Hooks:** kleine TypeScript-Module in einem Plugin, die Claude Code bei Ereignissen (etwa Sitzungsstart oder Tool-Aufruf) aufruft; der mitgelieferte Waechter ist so ein Mod.

## Was enthalten ist

| Teil | Ort im Paket | Zweck |
|---|---|---|
| Skill `orchestrator-starter` | `skills/orchestrator-starter/SKILL.md` | Rolle des Orchestrators, Auftragsaufbau, Modell-Routing, Berichte pruefen, Uebergabe |
| Regeln zum Skill | `skills/orchestrator-starter/regeln/` | `warteschlange.md`, `uebergabe.md`, `unbeaufsichtigt.md` |
| Waechter-Mod (Mod: siehe [Begriffe](#begriffe)) | `hooks/` | zeigt die Lauflaenge einer Sitzung an und erinnert an den Abschluss; verbietet nichts. Er erscheint in `claude plugin details` nicht als Hook (nur in `claude plugin validate`); ob er im echten Chat laedt, ist noch nicht ausprobiert |
| Skripte | `scripts/` | `post-neu.py` (neue Post an dein Fenster), `marker.py` ("wartet auf dich"-Marker), `test_post_neu.py`, `test_marker.py`, `LIESMICH.md` |
| Vorlagen | `vorlagen/` | `BEISPIEL-AUFTRAG.md`, `parallel.txt`, `repos-liste.txt` (Vorlage der Projektliste; deine Kopie heisst `belegung-projekte.txt`, siehe [Belegung](anleitungen/belegung.md)), `wartet-KUERZEL.txt` (Formatvorlage fuer den Marker; `marker.py` erzeugt die Datei selbst, du kopierst sie nicht) |
| Anleitungen | `anleitungen/` | [Warteschlange einrichten](anleitungen/warteschlange-einrichten.md), [Belegung](anleitungen/belegung.md), [Leitstand](anleitungen/leitstand.md), [Unbeaufsichtigt arbeiten](anleitungen/unbeaufsichtigt.md) |
| Schnellstart | [SCHNELLSTART.md](SCHNELLSTART.md) | in zehn Schritten bis zum ersten Auftrag |
| Beispiel | [beispiele/demo-durchlauf.md](beispiele/demo-durchlauf.md) | ein durchgespielter Strang `demo` |

Zu `unbeaufsichtigt` gehoert zusaetzlich die Regel unter `skills/orchestrator-starter/regeln/unbeaufsichtigt.md`.

## Was NICHT enthalten ist

- **Deploy:** keine Deploy-Regeln und keine Deploy-Skripte. Veroeffentlichen entscheidest immer du.
- **Erlaubnisregeln:** keine Rechte-Eintraege und kein Skript, das in deine Einstellungen schreibt. Ob Auto-Modus oder
  Warteschlange etwas ausfuehren duerfen, stellst du selbst ein. Wie Erlaubnisregeln aussehen, steht in der
  Claude-Code-Dokumentation zu Berechtigungen (https://code.claude.com/docs/en/permissions). Ein Lauf ohne passende
  Regeln lehnt die Aktion ab, statt nachzufragen.
- **Rechtstexte:** keine Datenschutz-, Impressum- oder Lizenztexte fuer deine Projekte.
- **Die Warteschlange selbst:** die Anleitung beschreibt, wie du sie baust; ein fertiges Programm liegt nicht bei.

## Voraussetzungen

- Claude Code (getestet mit 2.1.289; eine untere Grenze ist nicht bekannt, auch nicht fuer `claude plugin configure`
  und `claude plugin details`, die der Schnellstart benutzt).
- Internetzugang und `git` fuer die Installation: `claude plugin marketplace add` klont das Repository per HTTPS (so meldet
  es der Befehl). Ob die Installation auch ohne installiertes `git` geht, ist noch nicht ausprobiert.
- Python 3 fuer `post-neu.py` und `marker.py` (nur Standardbibliothek). Aufruf unter Windows `python`, sonst `python3`.
- Optional PowerShell 7 (`pwsh`), falls du die Windows-Aufgabenplanung nach der Anleitung benutzt. Das Werkzeug der
  Belegung liegt nicht bei; du baust es selbst (Python, nur Standardbibliothek, siehe [Belegung](anleitungen/belegung.md)).
- Teile der Warteschlange und der Aufgabenplanung sind **nur auf Windows** beschrieben; fuer Linux und macOS gibt die
  Anleitung die Alternative (cron, launchd). Skill, Post-Skript, Marker und Waechter sind nicht an Windows gebunden
  (getestet ist nur Windows, siehe "Bekannte Grenzen"). Pfade stehen im Text mit `\`; unter Linux und macOS schreibst du `/`.

## Installation

Die Installation schreibt in deine Nutzereinstellungen. Fuehre sie selbst aus, wenn du das Paket haben willst:

    claude plugin marketplace add dimensionwithin/orchestrator-starter
    claude plugin install orchestrator-starter@orchestrator-starter-marketplace

Den Berichte-Ordner setzt du als Plugin-Einstellung `berichte_ordner` (Typ Ordner); wie, steht in Schritt 3 des
Schnellstarts. Weiter mit [SCHNELLSTART.md](SCHNELLSTART.md).

## Sicherheitshinweis

Der Waechter-Mod ist ein Plugin mit Funktions-Hooks und **laeuft mit deinen Nutzerrechten**. Der Quelltext liegt offen unter
`hooks/` (`logic.ts`, `register.ts`, `waechter.test.ts`) und ist kurz; lies ihn vor der Installation. Er zeigt nur Hinweise
an, **sendet nichts** und verbietet nichts. Die Hooks sind TypeScript-Dateien, es gibt keinen Bauschritt: `hooks/hooks.json`
verweist auf `register.ts`, und `claude plugin test` laeuft ohne vorherigen Bau durch. Die Skripte unter `scripts/` sind ebenfalls lesbar und nutzen
nur die Python-Standardbibliothek. Pruefen kannst du das Paket in einem Klon des Repositories mit
`claude plugin validate <Ordner>` (Manifest) und `claude plugin test <Ordner>` (Tests des Waechters); die Tests der
Skripte laufen mit `python -m unittest` im Ordner `scripts/` (siehe [SCHNELLSTART.md](SCHNELLSTART.md)). Schreibe nie
Schluessel, Tokens oder Passwoerter in Auftraege, Berichte oder Post.

## Lizenz

MIT (siehe LICENSE).

## Support

Issues im Repository sind erwuenscht (Fehler, Fragen, Verbesserungsvorschlaege). Es gibt keine Zusage zu Antwortzeiten.
Die Nutzung erfolgt ohne Gewaehr, wie in der Lizenz beschrieben.

## Zeitzone

Die Zeitzone Berlin ist fest in `scripts/post-neu.py` eingebaut: Die Funktion `berlin_jetzt()` (Zeile 38 bis 51) liefert die
Ortszeit, in ihr steht `ZoneInfo("Europe/Berlin")` (Zeile 44). Wer eine andere Zeitzone braucht, aendert diese eine Zeile.
Die Rueckfallregel `berlin_regel()` (Zeile 28) gilt nur, falls `zoneinfo` fehlt, und muesste dann ebenfalls angepasst werden.

## Bekannte Grenzen

- Getestet wurde unter Windows. Linux und macOS sind ungetestet.
- Die Chat-Schritte 6 bis 10 des Schnellstarts (Orchestrator-Chat, Auftrag, Ausfuehrung, Berichtspruefung) sind am Text
  geprueft, aber noch nicht in einer angemeldeten Sitzung durchgespielt.
