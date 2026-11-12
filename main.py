# e2lite6 - a tiny chess engine with a 150k-node search.
import lzma, os
n = 0
for ch in open(os.path.join(os.path.dirname(__file__), "engine.b85")).read(): n = n * 95 + ord(ch) - 32
exec(lzma.decompress(n.to_bytes(3262, "big")))
