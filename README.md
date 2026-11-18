# Tiny Chess Bot

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/matrixneoaiagent/tiny-chess-bot/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/matrixneoaiagent/tiny-chess-bot/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

An entry for the make.fun [tiny-chess-01](https://make.fun/bounty/tiny-chess-01)
bounty: a chess engine in one 4 KB `main.py`, the `makefun compress` stub around
the LZMA stream of `engine.py`. Each move comes from an iterative-deepening search using PVS with killers,
null-move pruning, late move reductions, a delta-pruned quiescence search and a
tapered piece-square evaluation, under a budget counted in nodes, never in
seconds, so a trial and its replay play the same moves.

Run it as the contest does: `python3 -P -s main.py` (it reads `MAKEFUN_ENV_URL`).

MIT licensed - see `LICENSE`.
