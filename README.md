# tiny-chess-01

tiny-chess-01 is a submission-sized chess bot: its entry point must fit a 4,096-byte `main.py` and its whole repository an 8,192-byte cap.

## Layout

- `main.py` — the five-line loader; it decodes and executes the engine in memory.
- `engine.b85` — 3,972 ASCII characters encoding a 3,262-byte LZMA stream in base 95.

Each character contributes the digit `ord(c) - 32`; the loader accumulates one big integer, converts it to 3,262 big-endian bytes, and decompresses the result with `lzma`. Nothing is written to disk.

## Engine

`e2lite6` searches 150,000 nodes per move with iterative deepening, alpha-beta/PVS, a transposition table, null moves, late move reductions, and quiescence. Evaluation uses tapered piece-square tables plus pawn-structure terms.

The search is deterministic: fixed node budget, stable move ordering, and no randomness or wall-clock cutoffs.

Run it with `python3 main.py`; set `MAKEFUN_ENV_URL` to choose the match endpoint. MIT licensed — see `LICENSE`.
