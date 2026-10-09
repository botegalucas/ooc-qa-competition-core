"""Verify prepared package hashes. No model execution."""
import csv,hashlib
from pathlib import Path
r=Path(__file__).resolve().parent
with (r/"MANIFEST_SHA256.csv").open(encoding="utf-8",newline="") as f:rows=list(csv.DictReader(f))
for row in rows:
 p=r/row["relative_path"]
 assert p.exists(),row["relative_path"]
 assert hashlib.sha256(p.read_bytes()).hexdigest()==row["sha256"],row["relative_path"]
print("PACKAGE_HASH_PASS",len(rows))
