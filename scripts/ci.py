"""Select changed image projects and resolve their release tags (standard library only)."""

import json
from pathlib import Path
import re
import sys


def changed_projects(root, paths):
    projects = {
        path.parent.name for path in (root / "packages").glob("*/Dockerfile")
        if re.fullmatch(r"[a-z0-9]+(?:[._-][a-z0-9]+)*", path.parent.name)
    }
    shared = {"run.sh", "build.sh", "buildx.sh", "publish.sh", "scripts/ci.py", ".gitmodules",
              ".github/workflows/docker-publish.yml"}
    if shared.intersection(paths):
        return sorted(projects)
    return sorted({path.split("/")[1] for path in paths
                   if path.startswith("packages/") and len(path.split("/")) >= 2}
                  & projects)


def pull_request_paths(pages):
    files = [item for page in pages for item in page]
    # GitHub caps this endpoint at 3000 files; fail rather than silently omit images.
    if len(files) >= 3000:
        raise ValueError("PR file list reached GitHub's 3000-file limit")
    return [path for item in files
            for path in (item["filename"], item.get("previous_filename")) if path]


def release_tag(directory, commit):
    version = directory / "version"
    if version.exists() or version.is_symlink():
        # Only remove one line ending: blank lines and embedded CR must fail validation.
        tag = version.read_bytes().decode("ascii")
        if tag.endswith("\r\n"):
            tag = tag[:-2]
        elif tag.endswith("\n"):
            tag = tag[:-1]
    else:
        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise ValueError("Fallback must be a full commit SHA")
        tag = commit
    if tag == "latest" or not re.fullmatch(r"[a-zA-Z0-9_][a-zA-Z0-9_.-]{0,127}", tag):
        raise ValueError(f"Invalid release tag in {version}")
    return tag


def check_platforms(manifest):
    platforms = {f"{item['platform']['os']}/{item['platform']['architecture']}"
                 for item in manifest.get("manifests", [])}
    if not {"linux/amd64", "linux/arm64"}.issubset(platforms):
        raise ValueError(f"Published manifest is missing required platforms: {platforms}")


if __name__ == "__main__":
    if sys.argv[1] == "changed":
        paths = pull_request_paths(json.load(sys.stdin))
        print(json.dumps(changed_projects(Path.cwd(), paths)))
    elif sys.argv[1] == "tag":
        print(release_tag(Path(sys.argv[2]), sys.argv[3]))
    elif sys.argv[1] == "manifest":
        check_platforms(json.load(sys.stdin))
    else:
        sys.exit("Expected changed, tag or manifest")
