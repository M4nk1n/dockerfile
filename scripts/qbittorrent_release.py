"""Update the qBittorrent Enhanced Edition build version from its GitHub release."""

import json
from pathlib import Path
import re
import sys


def update_version(release, directory):
    tag = release["tag_name"]
    match = re.fullmatch(r"release-([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", tag) if isinstance(tag, str) else None
    if (release["draft"] is not False or release["prerelease"] is not False or not match):
        raise ValueError("Expected a stable qBittorrent Enhanced release tag such as release-5.2.4.10")
    version = match.group(1)
    version_file = directory / "version"
    changed = version_file.read_text().strip() != version
    if changed:
        version_file.write_text(version + "\n")
    return tag, changed


if __name__ == "__main__":
    tag, changed = update_version(json.load(sys.stdin), Path("packages/qbittorrent-enhanced"))
    print(f"tag={tag}")
    print(f"changed={str(changed).lower()}")
