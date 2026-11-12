# e2lite6: 150k-node chess engine loaded from a base-95 LZMA payload.
import lzma, os
n=0
for c in open(os.path.join(os.path.dirname(__file__), "engine.b85")).read(): n = n * 95 + ord(c) - 32
exec(lzma.decompress(n.to_bytes(3262, "big")))
