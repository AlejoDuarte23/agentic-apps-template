from agents import function_tool


@function_tool
def count_words(text: str) -> dict[str, int]:
    """Return simple text counts for deterministic checks."""
    words = [word for word in text.split() if word.strip()]
    return {
        "characters": len(text),
        "words": len(words),
    }
