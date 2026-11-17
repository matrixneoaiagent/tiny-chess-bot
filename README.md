# Tiny Chess Bot

A chess engine in one 4 KB `main.py`: the `makefun compress` stub around the
LZMA stream of `engine.py`. Each move comes from an iterative-deepening
alpha-beta search with PVS, killer moves, a quiescence search and a tapered
piece-square evaluation, under a budget counted in nodes, never in seconds, so
a trial and its replay play the same moves.

MIT licensed - see `LICENSE`.
