# Tiny Chess Bot

The whole entry is one self-contained `main.py`, about 4.0 KB: a base-95
ASCII payload plus its LZMA decoder. No second repository file is read.

Decoded, `e2lite6` runs a 150k-node alpha-beta search with quiescence,
MVV-LVA ordering, and tapered piece-square tables. It is deterministic
and never reads a clock.

Run it with `python3 main.py` from this directory.

MIT licensed — see `LICENSE`.
