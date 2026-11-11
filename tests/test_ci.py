import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from scripts.ci import changed_projects, check_platforms, push_paths, release_tag


REPO = Path(__file__).resolve().parents[1]
COMMIT = "a" * 40


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for project in ("one", "two"):
            directory = self.root / "packages" / project
            directory.mkdir(parents=True)
            (directory / "Dockerfile").write_text("FROM scratch\n")

    def test_project_selection(self):
        cases = [
            (["packages/one/file"], ["one"]),
            (["packages/one/a", "packages/two/b", "packages/one/c"], ["one", "two"]),
            (["README.md", "TASK.md"], []),
            (["packages/deleted/Dockerfile"], []),
            (["packages/one/old", "packages/two/new"], ["one", "two"]),
            (["packages/one/nested/Dockerfile"], ["one"]),
            (["packages/two"], ["two"]),
        ]
        for shared in ("run.sh", "build.sh", "buildx.sh", "publish.sh", "scripts/ci.py", ".gitmodules",
                       ".github/workflows/docker-publish.yml"):
            cases.append(([shared], ["one", "two"]))
        for paths, expected in cases:
            with self.subTest(paths=paths):
                self.assertEqual(changed_projects(self.root, paths), expected)

    def test_tag_fallback(self):
        self.assertEqual(release_tag(self.root, COMMIT), COMMIT)
        with self.assertRaises(ValueError):
            release_tag(self.root, "short")

    def test_manifest_requires_both_platforms(self):
        def manifest(architectures):
            return {"manifests": [{"platform": {"os": "linux", "architecture": arch}}
                                  for arch in architectures]}

        check_platforms(manifest(["amd64", "arm64"]))
        for value in ({}, manifest(["amd64"]), manifest(["arm64"])):
            with self.subTest(value=value), self.assertRaises(ValueError):
                check_platforms(value)

    def test_version_tags(self):
        for data in (b"1.2.3", b"1.2.3\n", b"1.2.3\r\n"):
            with self.subTest(data=data):
                (self.root / "version").write_bytes(data)
                self.assertEqual(release_tag(self.root, COMMIT), "1.2.3")
        for data in (b"", b"\n", b"1\n2", b"1\n\n", b"1\r2", b"a/b", b"-1",
                     b"latest", b"a" * 129, b"a b", b"$(echo hacked)", "版本".encode()):
            with self.subTest(data=data):
                (self.root / "version").write_bytes(data)
                with self.assertRaises((ValueError, UnicodeError)):
                    release_tag(self.root, COMMIT)

    def test_unreadable_version(self):
        (self.root / "version").mkdir()
        with self.assertRaises(OSError):
            release_tag(self.root, COMMIT)

    def test_broken_version_link(self):
        (self.root / "version").symlink_to(self.root / "missing")
        with self.assertRaises(OSError):
            release_tag(self.root, COMMIT)

    def prepare_scripts(self):
        for name in ("run.sh", "build.sh", "buildx.sh", "publish.sh"):
            shutil.copy2(REPO / name, self.root / name)
        shutil.copytree(REPO / "scripts", self.root / "scripts")
        (self.root / "packages/one/version").write_text("1.2.3\n")
        binary = self.root / "bin"
        binary.mkdir()
        docker = binary / "docker"
        docker.write_text('''#!/bin/bash
printf '%s\\n' "$*" >> "$DOCKER_LOG"
if [[ "$1" == build || "$1 $2" == 'buildx build' ]]; then
  exit "${BUILD_EXIT:-0}"
fi
''')
        docker.chmod(0o755)
        self.env = dict(os.environ, PATH=f"{binary}:{os.environ['PATH']}",
                        DOCKER_LOG=str(self.root / "docker.log"))

    def run_script(self, *args):
        return subprocess.run(["bash", str(self.root / "run.sh"), "-d", "one", "-a", "test",
                               *args], cwd="/tmp", env=self.env, text=True, capture_output=True)

    def test_multiplatform_once(self):
        self.prepare_scripts()
        result = self.run_script("-b", "-p", "--platform", "linux/amd64,linux/arm64")
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = (self.root / "docker.log").read_text().splitlines()
        self.assertEqual(len(calls), 1)
        self.assertIn("buildx build", calls[0])
        self.assertIn("test/one:latest", calls[0])
        self.assertIn("test/one:1.2.3", calls[0])
        self.assertIn("--platform=linux/amd64,linux/arm64", calls[0])
        self.assertIn("--push", calls[0])

    def test_regular_build_multiple_tags(self):
        self.prepare_scripts()
        result = self.run_script("-b", "-p", "-t", "1", "-t", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = (self.root / "docker.log").read_text().splitlines()
        self.assertEqual(len(calls), 4)
        self.assertIn("test/one:1", calls[1])
        self.assertIn("test/one:2", calls[2])
        self.assertEqual(calls[3], "push --all-tags test/one")

    def test_failed_build_never_pushes(self):
        self.prepare_scripts()
        self.env["BUILD_EXIT"] = "7"
        for extra in ([], ["--platform", "linux/amd64,linux/arm64"]):
            with self.subTest(extra=extra):
                (self.root / "docker.log").write_text("")
                result = self.run_script("-b", "-p", *extra)
                self.assertEqual(result.returncode, 7, result.stderr)
                calls = (self.root / "docker.log").read_text().splitlines()
                self.assertEqual(len(calls), 1)
                self.assertFalse(calls[0].startswith("push "))

    def test_invalid_version_never_builds(self):
        self.prepare_scripts()
        (self.root / "packages/one/version").write_text("")
        result = self.run_script("-b", "-p")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "docker.log").exists())

    def test_invalid_project_and_mode(self):
        self.prepare_scripts()
        for args in (["-d", "missing", "-b"], ["--platform", "linux/arm64", "-b"],
                     ["--platform", "linux/arm64", "-b", "-p", "--rm"]):
            with self.subTest(args=args):
                self.assertNotEqual(self.run_script(*args).returncode, 0)
                self.assertFalse((self.root / "docker.log").exists())

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def init_git(self):
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        return self.commit()

    def commit(self):
        self.git("add", ".")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def selected_between(self, before, after):
        output = subprocess.check_output([
            "python3", str(REPO / "scripts/ci.py"), "changed", before, after,
        ], cwd=self.root, text=True)
        return json.loads(output)

    def test_entire_push_includes_multiple_commits(self):
        before = self.init_git()
        (self.root / "packages/one/file").write_text("one")
        self.commit()
        (self.root / "packages/two/file").write_text("two")
        after = self.commit()
        self.assertEqual(self.selected_between(before, after), ["one", "two"])

    def test_move_checks_both_projects(self):
        (self.root / "packages/one/file").write_text("one")
        before = self.init_git()
        self.git("mv", "packages/one/file", "packages/two/file")
        self.assertEqual(self.selected_between(before, self.commit()), ["one", "two"])

    def test_initial_push_selects_all_existing_projects(self):
        after = self.init_git()
        self.assertEqual(self.selected_between("0" * 40, after), ["one", "two"])

    def test_docs_and_deleted_project(self):
        before = self.init_git()
        (self.root / "README.md").write_text("docs")
        self.assertEqual(self.selected_between(before, self.commit()), [])
        shutil.rmtree(self.root / "packages/one")
        self.assertEqual(self.selected_between(before, self.commit()), [])

    def test_force_push_compares_unrelated_tips(self):
        base = self.init_git()
        (self.root / "packages/one/file").write_text("one")
        before = self.commit()
        self.git("checkout", "-q", "-b", "replacement", base)
        (self.root / "packages/two/file").write_text("two")
        self.assertEqual(self.selected_between(before, self.commit()), ["one", "two"])

    def test_invalid_push_boundaries(self):
        with self.assertRaises(ValueError):
            push_paths("--invalid", COMMIT)


if __name__ == "__main__":
    unittest.main()
