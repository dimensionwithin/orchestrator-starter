"""demo-anlegen.py <Berichte-Ordner> <Arbeitsordner>

Legt den Beispielstrang `demo` an: den Auftrag demo-1 und die Uebergabe in den Berichte-Ordner,
dazu den leeren Arbeitsordner. Die Vorlagen liegen in ..\\beispiele\\demo neben diesem Skript.
Ueberschreibt nie: gibt es ein Ziel schon, wird nichts angelegt.
Rueckgabe: 0 angelegt, 2 falsche Angaben oder Berichte-Ordner fehlt, 3 Zieldatei gibt es schon.
Nur Standardbibliothek.
"""
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
VORLAGEN = os.path.join(HIER, "..", "beispiele", "demo")


def main(argv):
    if len(argv) != 2:
        print("demo-anlegen: Aufruf: python demo-anlegen.py <Berichte-Ordner> <Arbeitsordner>")
        return 2
    berichte = os.path.abspath(argv[0])
    arbeit = os.path.abspath(argv[1])
    print("demo-anlegen: Berichte-Ordner " + berichte)
    if not os.path.isdir(berichte):
        print("demo-anlegen: Berichte-Ordner fehlt: " + berichte)
        return 2

    ziele = [
        (os.path.join(VORLAGEN, "auftraege", "demo-1.md"),
         os.path.join(berichte, "auftraege", "demo-1.md")),
        (os.path.join(VORLAGEN, "UEBERGABE-demo.md"),
         os.path.join(berichte, "UEBERGABE-demo.md")),
    ]
    vorhanden = [z for _, z in ziele if os.path.exists(z)]
    if vorhanden:
        for z in vorhanden:
            print("demo-anlegen: gibt es schon, nichts ueberschrieben: " + z)
        return 3

    texte = []
    for quelle, ziel in ziele:
        with open(quelle, encoding="utf-8", newline="") as f:
            text = f.read()
        text = text.replace("<Berichte-Ordner>", berichte).replace("<Arbeitsordner>", arbeit)
        texte.append((ziel, text))

    for ziel, text in texte:
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "x", encoding="utf-8", newline="") as f:
            f.write(text)
        print("demo-anlegen: angelegt " + ziel)
    os.makedirs(arbeit, exist_ok=True)
    print("demo-anlegen: angelegt " + arbeit)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
