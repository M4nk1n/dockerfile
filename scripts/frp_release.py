"""Validate the latest stable frp release and update the build input."""

import json
from pathlib import Path
import re
import sys


def update_version(release, directory):
    tag = release["tag_name"]
    if (release["draft"] is not False or release["prerelease"] is not False
            or not isinstance(tag, str)
            or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag)):
        raise ValueError("Expected a stable frp release tag such as v0.72.0")
    version = tag[1:]
    version_file = directory / "version"
    changed = version_file.read_text().strip() != version
    if changed:
        version_file.write_text(version + "\n")
    return tag, changed


if __name__ == "__main__":
    tag, changed = update_version(json.load(sys.stdin), Path("packages/frp"))
    print(f"tag={tag}")
    print(f"changed={str(changed).lower()}")
