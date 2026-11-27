from pathlib import Path
import tempfile
import unittest

from scripts.ci import changed_projects, release_tag
from scripts.aria_release import update_version


class AriaReleaseTests(unittest.TestCase):
    def test_new_release_updates_version(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "version").write_text("1.3.14\n")
            release = dict(tag_name="1.3.15", draft=False, prerelease=False)
            self.assertEqual(update_version(release, directory), ("1.3.15", True))
            self.assertEqual((directory / "version").read_text(), "1.3.15\n")
            self.assertEqual(update_version(release, directory), ("1.3.15", False))

    def test_invalid_releases_do_not_change_version(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            version = directory / "version"
            version.write_text("1.3.14\n")
            cases = [dict(tag_name=tag, draft=False, prerelease=False) for tag in
                     ("", "v1.3.15", "1.3.15-rc.1", "1.3.15\ninjected=true", "$(id)", None)]
            cases += [dict(tag_name="1.3.15", draft=True, prerelease=False),
                      dict(tag_name="1.3.15", draft=False, prerelease=True), {}]
            for release in cases:
                with self.subTest(release=release), self.assertRaises((ValueError, KeyError)):
                    update_version(release, directory)
                self.assertEqual(version.read_text(), "1.3.14\n")

    def test_version_commit_selects_aria_for_existing_publisher(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(changed_projects(root, ["packages/aria/version"]), ["aria"])
        self.assertEqual(release_tag(root / "packages/aria", "a" * 40), "1.3.15")


if __name__ == "__main__":
    unittest.main()
