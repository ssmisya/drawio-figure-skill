#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"

find "$TARGET" -name '*.drawio' -print0 | while IFS= read -r -d '' file; do
  python - "$file" <<'PY'
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

p = Path(sys.argv[1])
root = ET.parse(p).getroot()
assert root.tag == "mxfile", f"{p}: root is {root.tag}, expected mxfile"
pages = root.findall("diagram")
assert pages, f"{p}: no diagrams"
print(f"drawio ok: {p} ({len(pages)} page(s), {p.stat().st_size} bytes)")
PY
done

find "$TARGET" -name '*.pptx' -print0 | while IFS= read -r -d '' file; do
  unzip -t "$file" >/dev/null
  echo "pptx ok: $file"
done
