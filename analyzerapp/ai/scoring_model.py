"""Simple, transparent interview rubric scoring helper."""


def calculate_score(communication: int, relevance: int, confidence: int) -> float:
    scores = (communication, relevance, confidence)
    if any(not isinstance(value, int) for value in scores):
        raise TypeError("Scores must be integers.")
    if any(value < 0 or value > 100 for value in scores):
        raise ValueError("Each score must be between 0 and 100.")
    return round(sum(scores) / len(scores), 2)
