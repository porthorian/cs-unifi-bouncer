"""Fail builds if ko silently omits a supported platform from the OCI layout."""

import json
from pathlib import Path
import sys

layout = Path(sys.argv[1])
index = json.loads((layout / "index.json").read_text())
platforms = set()
for descriptor in index["manifests"]:
    algorithm, digest = descriptor["digest"].split(":", 1)
    image = json.loads((layout / "blobs" / algorithm / digest).read_text())
    for manifest in image.get("manifests", [descriptor]):
        platform = manifest["platform"]
        platforms.add((platform["os"], platform["architecture"]))

expected = {("linux", "amd64"), ("linux", "arm64"), ("linux", "arm")}
if platforms != expected:
    raise SystemExit(f"Image platforms {sorted(platforms)} differ from {sorted(expected)}")
print("Verified image platforms:", sorted(platforms))
