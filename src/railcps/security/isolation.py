def isolated_sources(trust_scores: dict[str, float], threshold: float = 0.45) -> set[str]:
    return {src for src, score in trust_scores.items() if score < threshold}
