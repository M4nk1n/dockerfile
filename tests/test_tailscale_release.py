from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.ci import changed_projects, release_tag
from scripts.tailscale_release import update_version


class TailscaleReleaseTests(unittest.TestCase):
    def test_new_version_is_the_build_and_image_tag(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "version").write_text("v1.104.5\n")
            release = dict(tag_name="v1.104.6", draft=False, prerelease=False)
            self.assertEqual(update_version(release, directory), ("v1.104.6", True))
            self.assertEqual(release_tag(directory, "a" * 40), "v1.104.6")
            self.assertEqual(update_version(release, directory), ("v1.104.6", False))

    def test_invalid_releases_do_not_change_build_input(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            version = directory / "version"
            version.write_text("v1.104.5\n")
            cases = [dict(tag_name=tag, draft=False, prerelease=False) for tag in
                     ("", "latest", "v1.105.0-pre", "v1.2.3\ninjected=true", "$(id)", None)]
            cases += [dict(tag_name="v1.104.6", draft=True, prerelease=False),
                      dict(tag_name="v1.104.6", draft=False, prerelease=True), {}]
            for release in cases:
                with self.subTest(release=release), self.assertRaises((ValueError, KeyError)):
                    update_version(release, directory)
                self.assertEqual(version.read_text(), "v1.104.5\n")

    def test_derper_uses_existing_push_selection(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(changed_projects(root, ["packages/derper/version"]), ["derper"])
        self.assertEqual(changed_projects(root, [".github/workflows/derper-release.yml"]), [])

    def test_version_commit_selects_only_derper_for_existing_publisher(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            def git(*args):
                return subprocess.check_output([
                    "git", "-C", temp, "-c", "user.name=Test", "-c", "user.email=test@example.com",
                    "-c", "commit.gpgsign=false", *args,
                ], text=True).strip()

            for project in ("derper", "other"):
                directory = root / "packages" / project
                directory.mkdir(parents=True)
                (directory / "Dockerfile").write_text("FROM scratch\n")
            directory = root / "packages/derper"
            (directory / "version").write_text("v1.104.5\n")
            git("init", "-q")
            git("add", ".")
            git("commit", "-qm", "initial")
            before = git("rev-parse", "HEAD")
            update_version(dict(tag_name="v1.104.6", draft=False, prerelease=False), directory)
            git("add", "packages/derper/version")
            git("commit", "-qm", "chore(derper): update to v1.104.6")
            after = git("rev-parse", "HEAD")
            selected = subprocess.check_output([
                "python3", str(repo / "scripts/ci.py"), "changed", before, after,
            ], cwd=root, text=True).strip()
            self.assertEqual(selected, '["derper"]')
            self.assertEqual(git("show", "HEAD:packages/derper/version"), "v1.104.6")


if __name__ == "__main__":
    unittest.main()
