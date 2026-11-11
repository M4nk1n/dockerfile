"""Validate the latest stable release and update the derper build input."""

import json
from pathlib import Path
import re
import sys


def update_version(release, directory):
    tag = release["tag_name"]
    if (release["draft"] is not False or release["prerelease"] is not False
            or not isinstance(tag, str)
            or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag)):
        raise ValueError("Expected a stable Tailscale release tag such as v1.104.6")
    version = directory / "version"
    changed = version.read_text().strip() != tag
    if changed:
        version.write_text(tag + "\n")
    return tag, changed


if __name__ == "__main__":
    tag, changed = update_version(json.load(sys.stdin), Path("packages/derper"))
    print(f"tag={tag}")
    print(f"changed={str(changed).lower()}")
