from pathlib import Path
import tempfile
import unittest

from scripts.ci import changed_projects, release_tag
from scripts.frp_release import update_version


class FrpReleaseTests(unittest.TestCase):
    def test_new_release_updates_version_without_v_prefix(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "version").write_text("0.71.0\n")
            release = dict(tag_name="v0.72.0", draft=False, prerelease=False)
            self.assertEqual(update_version(release, directory), ("v0.72.0", True))
            self.assertEqual((directory / "version").read_text(), "0.72.0\n")
            self.assertEqual(update_version(release, directory), ("v0.72.0", False))

    def test_invalid_releases_do_not_change_version(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            version = directory / "version"
            version.write_text("0.71.0\n")
            cases = [dict(tag_name=tag, draft=False, prerelease=False) for tag in
                     ("", "v0.72.0-rc.1", "v1.2.3\ninjected=true", "$(id)", None)]
            cases += [dict(tag_name="v0.72.0", draft=True, prerelease=False),
                      dict(tag_name="v0.72.0", draft=False, prerelease=True), {}]
            for release in cases:
                with self.subTest(release=release), self.assertRaises((ValueError, KeyError)):
                    update_version(release, directory)
                self.assertEqual(version.read_text(), "0.71.0\n")

    def test_version_commit_selects_frp_for_existing_publisher(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(changed_projects(root, ["packages/frp/version"]), ["frp"])
        self.assertEqual(release_tag(root / "packages/frp", "a" * 40), "0.72.0")


if __name__ == "__main__":
    unittest.main()
