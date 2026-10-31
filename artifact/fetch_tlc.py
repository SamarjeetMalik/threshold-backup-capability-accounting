"""Fetch the official, checksum-pinned TLC jar; no other dependency is installed."""
from pathlib import Path
import hashlib
import urllib.request
from run_tlc import PINNED_SHA256

url = "https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar"
target = Path(__file__).resolve().parent / ".tools/tla2tools.jar"
target.parent.mkdir(exist_ok=True)
if target.exists():
    data = target.read_bytes()
else:
    with urllib.request.urlopen(url, timeout=120) as response:
        data = response.read()
if hashlib.sha256(data).hexdigest() != PINNED_SHA256:
    raise SystemExit("Checksum mismatch; unverified download is not written")
target.write_bytes(data)
print(target)
print("Verified SHA-256:", PINNED_SHA256)
