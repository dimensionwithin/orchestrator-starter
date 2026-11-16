"""Tests fuer demo-anlegen.py. Jeder Test startet das Skript als eigenen Prozess in einem Temp-Ordner."""
import os
import subprocess
import sys
import tempfile
import unittest

SKRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo-anlegen.py")


def lauf(*args):
    return subprocess.run(
        [sys.executable, "-B", SKRIPT, *args],
        capture_output=True, text=True, timeout=60,
    )


class DemoAnlegenTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.berichte = os.path.join(self._tmp.name, "berichte")
        self.arbeit = os.path.join(self._tmp.name, "arbeit")
        os.mkdir(self.berichte)

    def test_legt_drei_ziele_an(self):
        r = lauf(self.berichte, self.arbeit)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.isfile(os.path.join(self.berichte, "auftraege", "demo-1.md")))
        self.assertTrue(os.path.isfile(os.path.join(self.berichte, "UEBERGABE-demo.md")))
        self.assertTrue(os.path.isdir(self.arbeit))
        self.assertEqual(os.listdir(self.arbeit), [])
        zeilen = r.stdout.splitlines()
        self.assertEqual(zeilen[0], "demo-anlegen: Berichte-Ordner " + self.berichte)
        self.assertEqual(sum(1 for z in zeilen if z.startswith("demo-anlegen: angelegt ")), 3)

    def test_ersetzt_platzhalter(self):
        lauf(self.berichte, self.arbeit)
        for ziel in (os.path.join(self.berichte, "auftraege", "demo-1.md"),
                     os.path.join(self.berichte, "UEBERGABE-demo.md")):
            with open(ziel, encoding="utf-8") as f:
                text = f.read()
            self.assertNotIn("<Berichte-Ordner>", text)
            self.assertNotIn("<Arbeitsordner>", text)
        with open(os.path.join(self.berichte, "auftraege", "demo-1.md"), encoding="utf-8") as f:
            self.assertIn(self.arbeit + "\\rechner.py", f.read())

    def test_ueberschreibt_nie(self):
        self.assertEqual(lauf(self.berichte, self.arbeit).returncode, 0)
        ziel = os.path.join(self.berichte, "auftraege", "demo-1.md")
        with open(ziel, "rb") as f:
            vorher = f.read()
        r = lauf(self.berichte, self.arbeit)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("demo-anlegen: gibt es schon, nichts ueberschrieben: ", r.stdout)
        with open(ziel, "rb") as f:
            self.assertEqual(f.read(), vorher)

    def test_fehlender_berichte_ordner(self):
        fehlt = os.path.join(self._tmp.name, "gibt-es-nicht")
        r = lauf(fehlt, self.arbeit)
        self.assertEqual(r.returncode, 2)
        self.assertIn("demo-anlegen: Berichte-Ordner fehlt: " + fehlt, r.stdout)


if __name__ == "__main__":
    unittest.main()
