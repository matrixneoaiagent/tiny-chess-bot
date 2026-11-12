# tiny-chess-bot

Self-contained entry for the tiny-chess-01 task.

- `main.py` is the entire entry (~3.6 KB); no second repository file is read.
- The engine is embedded as a latin-1 base-252 payload decoded inline at startup.
- Engine: 150k-node alpha-beta with quiescence, MVV-LVA ordering, tapered PSTs.
- Deterministic: fixed node budget, no clock reads, reproducible output.
- Python 3.13 standard library only.

Run: `python3 -P -s main.py`

MIT license.
