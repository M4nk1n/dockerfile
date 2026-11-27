from pathlib import Path
import unittest
import tempfile

from scripts.ci import changed_projects, release_tag
from scripts.volto_release import update_version


class VoltoReleaseTests(unittest.TestCase):
    def test_new_release_updates_build_and_image_version_without_v_prefix(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / "version").write_text("1.7.0\n")
            release = dict(tag_name="v1.8.5", draft=False, prerelease=False)
            self.assertEqual(update_version(release, directory), ("v1.8.5", True))
            self.assertEqual((directory / "version").read_text(), "1.8.5\n")
            self.assertEqual(release_tag(directory, "a" * 40), "1.8.5")
            self.assertEqual(update_version(release, directory), ("v1.8.5", False))

    def test_invalid_releases_do_not_change_build_input(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            version = directory / "version"
            version.write_text("1.7.0\n")
            cases = [dict(tag_name=tag, draft=False, prerelease=False) for tag in
                     ("", "v1.8.5-rc.1", "v1.2.3\ninjected=true", "$(id)", None)]
            cases += [dict(tag_name="v1.8.5", draft=True, prerelease=False),
                      dict(tag_name="v1.8.5", draft=False, prerelease=True), {}]
            for release in cases:
                with self.subTest(release=release), self.assertRaises((ValueError, KeyError)):
                    update_version(release, directory)
                self.assertEqual(version.read_text(), "1.7.0\n")

    def test_version_commit_selects_volto_for_existing_publisher(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(changed_projects(root, ["packages/volto/version"]), ["volto"])
        self.assertEqual(release_tag(root / "packages/volto", "a" * 40), "1.7.0")


if __name__ == "__main__":
    unittest.main()
