# tiny-chess-01 engine

A deterministic, standard-library-only chess engine for make.fun's tiny-chess-01.
The competition plays 16 games per trial against eight house engines (depth-2,
depth-3, depth-4 and node-capped alpha-beta searches from 100k to 2M nodes),
scored as Elo; the entry is capped at 4,096 bytes for `main.py` and 8,192
bytes for the whole repository, and may not call a model or the network.

`main.py` is the whole entry: it unpacks a compressed payload and speaks the
contest env protocol (`POST /game`, `POST /move`). It searches 150,000 nodes
per move with iterative deepening, alpha-beta/PVS, a transposition table, null
moves and late move reductions, quiescence, and a tapered piece-square plus
pawn-structure evaluation. It never reads a clock, so live and replay choose
the same moves.

Run: `MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 -P -s main.py`.

License: MIT (see `LICENSE`).
