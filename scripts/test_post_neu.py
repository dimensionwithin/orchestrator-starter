"""Tests fuer post-neu.py. Aufruf im Ordner scripts: python3 -m unittest -v
(unter Windows ggf. python statt python3). Alles in einem Wegwerfordner, nichts ausserhalb.
Die Tests starten das Skript als eigenen Prozess, also durch dieselbe Schicht wie im Alltag."""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SKRIPT = pathlib.Path(__file__).resolve().parent / "post-neu.py"

GUTER_KOPF = "## 01.01.2030 12:00 — an B — Probe"
SCHLECHTER_KOPF = "## 01.01.2030 12:00 - an B - Probe"


def kopiere_skript(ordner):
    """Legt eine Kopie des Skripts nach <ordner>\\scripts\\ und gibt ihren Pfad zurueck."""
    ziel = pathlib.Path(ordner) / "scripts"
    ziel.mkdir(parents=True)
    kopie = ziel / "post-neu.py"
    shutil.copyfile(SKRIPT, kopie)
    return kopie


def lauf(skript, *args):
    return subprocess.run([sys.executable, "-B", str(skript), *args], capture_output=True, text=True,
                          encoding="utf-8", stdin=subprocess.DEVNULL, timeout=60)


def schreibe_post(basis, kopf):
    post = pathlib.Path(basis) / "post"
    post.mkdir(exist_ok=True)
    (post / "VON-A.md").write_text("# Post von A\n\n---\n\n%s\n\nHallo B\n" % kopf,
                                   encoding="utf-8", newline="\n")


class PostNeuTest(unittest.TestCase):
    def test_kopf_mit_bindestrich_wird_gemeldet_und_die_marke_nicht_gesetzt(self):
        with tempfile.TemporaryDirectory() as tmp:
            basis = pathlib.Path(tmp).resolve() / "berichte"
            skript = kopiere_skript(basis)
            schreibe_post(basis, SCHLECHTER_KOPF)
            marke = basis / "post" / "gelesen" / "B.txt"
            r = lauf(skript, "B")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("VON-A.md", r.stdout)                  # Dateiname
            self.assertIn("Zeile 5", r.stdout)                   # Zeilennummer (Kopf steht in Zeile 5)
            self.assertIn("—", r.stdout)                    # Hinweis auf den langen Gedankenstrich
            self.assertFalse(marke.exists(), "Lesemarke darf bei unlesbarer Kopfzeile nicht gesetzt werden")
            # Kopf korrigiert: der Eintrag erscheint, die Marke wird gesetzt.
            schreibe_post(basis, GUTER_KOPF)
            r = lauf(skript, "B")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("Hallo B", r.stdout)
            self.assertNotIn("nicht lesbar", r.stdout)
            self.assertTrue(marke.is_file())

    def test_erste_ausgabezeile_nennt_den_berichte_ordner_auch_am_falschen_ort(self):
        with tempfile.TemporaryDirectory() as tmp:
            falschort = pathlib.Path(tmp).resolve() / "falschort"
            skript = kopiere_skript(falschort)
            r = lauf(skript, "B", "--nur-zeigen")
            self.assertEqual(r.returncode, 0, r.stderr)
            erste = r.stdout.splitlines()[0]
            self.assertIn(str(falschort), erste)


if __name__ == "__main__":
    unittest.main()
