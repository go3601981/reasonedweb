#!/usr/bin/env python3
"""Regression tests for verificar_assets.py's progressive-video references."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("verificar_assets.py")


class VideoAssetReferencesTest(unittest.TestCase):
    def setUp(self) -> None:
        # Keep fixtures beside the test so Windows sandboxing never redirects
        # them to a package temp directory that the test process cannot write.
        self.tempdir = tempfile.TemporaryDirectory(
            prefix=".tmp-verificar-assets-", dir=SCRIPT.parent
        )
        self.root = Path(self.tempdir.name)
        (self.root / "site" / "assets").mkdir(parents=True)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--raiz", "site"],
            cwd=self.root,
            capture_output=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )

    def write_player(self) -> None:
        (self.root / "site" / "index.html").write_text(
            '<a href="assets/film.mp4" data-poster="assets/poster.webp" '
            'data-en="assets/film.en.vtt" data-es="assets/film.es.vtt">Film</a>',
            encoding="utf-8",
        )
        (self.root / "site" / "assets" / "film.mp4").write_bytes(b"video")
        (self.root / "site" / "assets" / "poster.webp").write_bytes(b"poster")
        (self.root / "site" / "assets" / "film.en.vtt").write_text(
            "WEBVTT\n\n00:00.000 --> 00:01.000\nEnglish\n", encoding="utf-8"
        )

    def track_all(self) -> None:
        subprocess.run(["git", "add", "site"], cwd=self.root, check=True)

    def test_missing_data_es_caption_fails(self) -> None:
        self.write_player()
        self.track_all()

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("assets/film.es.vtt", result.stdout)
        self.assertIn("4 referencia(s) local(es)", result.stdout)

    def test_all_video_assets_present_and_tracked_passes(self) -> None:
        self.write_player()
        (self.root / "site" / "assets" / "film.es.vtt").write_text(
            "WEBVTT\n\n00:00.000 --> 00:01.000\nEspañol\n", encoding="utf-8"
        )
        self.track_all()

        result = self.run_validator()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("4 referencia(s) local(es)", result.stdout)

    def test_empty_caption_fails(self) -> None:
        self.write_player()
        (self.root / "site" / "assets" / "film.es.vtt").touch()
        self.track_all()

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("0 bytes", result.stdout)
        self.assertIn("assets/film.es.vtt", result.stdout)

    def test_untracked_caption_fails(self) -> None:
        self.write_player()
        (self.root / "site" / "assets" / "film.es.vtt").write_text(
            "WEBVTT\n\n00:00.000 --> 00:01.000\nEspañol\n", encoding="utf-8"
        )
        self.track_all()
        subprocess.run(
            ["git", "reset", "-q", "site/assets/film.es.vtt"],
            cwd=self.root,
            check=True,
        )

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("site/assets/film.es.vtt", result.stdout)
        self.assertIn("GIT NO LOS SIGUE", result.stdout)


if __name__ == "__main__":
    unittest.main()
