"""Kleine Tests fuer marker.py. Aufruf im Ordner scripts: python3 -m unittest -v
(unter Windows ggf. python statt python3). Alles in einem Wegwerfordner, nichts ausserhalb."""
import datetime
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

import marker

SKRIPT = pathlib.Path(marker.__file__).resolve()


class MarkerTest(unittest.TestCase):
    def test_setze_marker_schreibt_zeitstempel_und_einzeiligen_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            jetzt = datetime.datetime(2030, 1, 2, 3, 4)
            ziel = marker.setze_marker(tmp, "demo", "Frage\nzur  Wahl", jetzt)
            self.assertEqual(ziel, pathlib.Path(tmp) / "leitstand" / "wartet-demo.txt")
            self.assertEqual(ziel.read_bytes(), b"2030-01-02 03:04\nFrage zur Wahl\n")
            with self.assertRaises(ValueError):
                marker.setze_marker(tmp, "../boese", "x")

    def test_aufruf_ueber_die_befehlszeile_mit_berichte_parameter(self):
        with tempfile.TemporaryDirectory() as tmp:
            def lauf(*args):
                return subprocess.run([sys.executable, str(SKRIPT), "--berichte", tmp, *args], capture_output=True,
                                      text=True, encoding="utf-8", stdin=subprocess.DEVNULL, timeout=60)
            r = lauf("demo", "Entscheidung offen")
            self.assertEqual(r.returncode, 0, r.stderr)
            datei = pathlib.Path(tmp) / "leitstand" / "wartet-demo.txt"
            self.assertEqual(datei.read_text(encoding="utf-8").splitlines()[1], "Entscheidung offen")
            self.assertIn("Entscheidung offen", r.stdout)       # die Ausgabe zeigt die Datei zur Kontrolle
            r = lauf("demo", "--keine")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(datei.read_text(encoding="utf-8").splitlines()[1], "keine")
            self.assertEqual(lauf("demo").returncode, 1)         # weder Text noch --keine: Fehler, nichts geaendert

    def test_erste_ausgabezeile_nennt_den_berichte_ordner_auch_am_falschen_ort(self):
        with tempfile.TemporaryDirectory() as tmp:
            falschort = pathlib.Path(tmp).resolve() / "falschort"
            (falschort / "scripts").mkdir(parents=True)
            kopie = falschort / "scripts" / "marker.py"
            shutil.copyfile(SKRIPT, kopie)
            r = subprocess.run([sys.executable, "-B", str(kopie), "demo", "Probe"], capture_output=True,
                               text=True, encoding="utf-8", stdin=subprocess.DEVNULL, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout.splitlines()[0], "marker: Berichte-Ordner %s" % falschort)

    def test_text_mit_fuehrendem_minus_verweist_auf_zwei_striche(self):
        with tempfile.TemporaryDirectory() as tmp:
            def lauf(*args):
                return subprocess.run([sys.executable, "-B", str(SKRIPT), "--berichte", tmp, *args],
                                      capture_output=True, text=True, encoding="utf-8",
                                      stdin=subprocess.DEVNULL, timeout=60)
            r = lauf("demo", "-x")
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("'--'", r.stderr)                      # die Meldung nennt den Ausweg
            self.assertFalse((pathlib.Path(tmp) / "leitstand").exists())   # nichts geschrieben
            r = lauf("demo", "--", "-x")                         # der genannte Ausweg funktioniert
            self.assertEqual(r.returncode, 0, r.stderr)
            datei = pathlib.Path(tmp) / "leitstand" / "wartet-demo.txt"
            self.assertEqual(datei.read_text(encoding="utf-8").splitlines()[1], "-x")


if __name__ == "__main__":
    unittest.main()
