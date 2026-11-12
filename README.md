# tiny-chess-01

tiny-chess-01 is a minimal chess engine packed under an 8,192-byte repository
cap, with `main.py` itself capped at 4,096 bytes.

The code is split: `main.py` is a five-line loader that reads base-95 text
from `engine.b85`, rebuilds an LZMA stream, and executes the engine.

e2lite6 searches up to 150,000 nodes using iterative deepening, alpha-beta
with PVS, a transposition table, null moves, late move reductions, and
quiescence search; evaluation uses tapered piece-square tables and
pawn-structure terms.

It is deterministic — no randomness or time-based cutoffs — so the same
position always yields the same move.

Run it with `python3 main.py` (Python 3.13, standard library only). MIT
licensed; see `LICENSE`.
