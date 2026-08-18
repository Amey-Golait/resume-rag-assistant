import hashlib
import math
import re

DEFAULT_EMBEDDING_MODEL = "local-hashing"
EMBEDDING_DIMENSIONS = 384
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}")


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def _token_index(token: str) -> int:
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=4).digest()
    return int.from_bytes(digest, "big") % EMBEDDING_DIMENSIONS


def _embed_text(text: str) -> list[float]:
    vector = [0.0] * EMBEDDING_DIMENSIONS
    for token in _tokenize(text):
        vector[_token_index(token)] += 1.0

    magnitude = math.sqrt(sum(value * value for value in vector))
    if not magnitude:
        return vector

    return [value / magnitude for value in vector]


def generate_embeddings(
    chunks: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> list[list[float]]:
    return [_embed_text(chunk) for chunk in chunks]
