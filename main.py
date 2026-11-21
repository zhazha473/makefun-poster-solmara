"""the-poster-for-a-place-that-i-2-20261121-0539 entry: "Winding the Sun at Solmara".

Writes one image to /output/entry.png: a vintage art-deco travel poster
for SOLMARA, the bay where the sun is wound by hand — a great brass
clockwork sun low over a calm teal bay at golden dawn, a tiny keeper on
a ladder turning a huge brass key in the sun's side, a winding tower on
the cliff, small sailboats, gulls. The only text in the image is the
invented place name "SOLMARA".

Deterministic: byte-for-byte copy of entry.png shipped in this repository.
No network, no randomness, no model calls, no clock. Two runs write the
exact same bytes.
"""

import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    with open(DST, "wb") as f:
        f.write(data)
    # Self-check: the written file must be byte-identical to the source.
    if os.path.getsize(DST) != len(data):
        raise SystemExit("output size mismatch: wrote %d bytes, expected %d"
                         % (os.path.getsize(DST), len(data)))
    with open(DST, "rb") as f:
        written = f.read()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        raise SystemExit("output hash mismatch: written file differs from source")
    print("Wrote %s (%d bytes, sha256 %s)"
          % (DST, len(data), hashlib.sha256(data).hexdigest()[:16]))


if __name__ == "__main__":
    main()
