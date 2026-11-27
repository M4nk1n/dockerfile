"""Validate the latest stable AriaNg release and update the build input."""

import json
from pathlib import Path
import re
import sys


def update_version(release, directory):
    tag = release["tag_name"]
    if (release["draft"] is not False or release["prerelease"] is not False
            or not isinstance(tag, str)
            or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", tag)):
        raise ValueError("Expected a stable AriaNg release tag such as 1.3.15")
    version_file = directory / "version"
    changed = version_file.read_text().strip() != tag
    if changed:
        version_file.write_text(tag + "\n")
    return tag, changed


if __name__ == "__main__":
    tag, changed = update_version(json.load(sys.stdin), Path("packages/aria"))
    print(f"tag={tag}")
    print(f"changed={str(changed).lower()}")
