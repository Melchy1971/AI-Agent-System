import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(x ** 2 for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def top_k(query_vec: list[float], corpus: list[tuple[str, list[float]]], k: int = 5) -> list[str]:
    scored = [(doc, cosine_similarity(query_vec, vec)) for doc, vec in corpus]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored[:k]]
