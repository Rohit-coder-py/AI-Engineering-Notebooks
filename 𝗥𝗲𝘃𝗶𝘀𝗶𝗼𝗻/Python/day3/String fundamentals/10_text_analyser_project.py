"""
================================================================================
DAY 3 - DAILY PRACTICE PROJECT: TEXT ANALYSER
================================================================================

OBJECTIVE
---------
Build a small reusable program that analyses a paragraph and reports:
  * character count (with and without spaces)
  * word count
  * sentence count
  * most frequent word
  * vowel and consonant counts
  * whether a chosen word appears

DESIGN
------
* One function = one responsibility.
* Pure functions for calculations; I/O only in main().
* Return values, not prints, from the analysis functions.
* Docstrings + type hints on every public function.

STATED ASSUMPTIONS
------------------
1. CHARACTER: a Unicode code point. "With spaces" counts everything;
   "without spaces" excludes whitespace (spaces, tabs, newlines).
2. WORD: a whitespace-separated token after trimming edge punctuation.
   Tokens that become empty after trimming are ignored.
   Internal punctuation (apostrophes, hyphens) is preserved:
   "don't" and "well-known" are single words.
3. SENTENCE: a chunk of text ending with '.', '!' or '?'. Runs of
   terminators (e.g. "...") count as one boundary. Trailing text without a
   terminator counts as a sentence. Abbreviations ("Dr.", "e.g.") are NOT
   handled - this is documented as a limitation.
4. CASE: word-frequency analysis is case-insensitive (casefolded).
5. WHITESPACE: normalised to single spaces BEFORE analysis, so the reported
   character count is the normalised count, not the raw input count.
================================================================================
"""

from __future__ import annotations

import re
import string
from collections import Counter

# Punctuation removed from the EDGES of a token only.
EDGE_PUNCTUATION = string.punctuation
VOWELS = frozenset("aeiou")
SENTENCE_BOUNDARY = re.compile(r"[.!?]+")


# ------------------------------------------------------------------------------
# TEXT CLEANING
# ------------------------------------------------------------------------------
def normalize_whitespace(text: str) -> str:
    """Collapse all whitespace runs into single spaces and trim the ends.

    Args:
        text: Raw input text.

    Returns:
        Text with single spaces and no leading/trailing whitespace.
    """
    return " ".join(text.split())


def tokenize(text: str) -> list[str]:
    """Split text into normalised words.

    Each whitespace-separated token is stripped of edge punctuation and
    casefolded. Empty tokens are dropped.

    Args:
        text: Raw or normalised text.

    Returns:
        A list of cleaned, lowercase words.
    """
    words = []
    for raw in normalize_whitespace(text).split():
        word = raw.strip(EDGE_PUNCTUATION).casefold()
        if word:
            words.append(word)
    return words


# ------------------------------------------------------------------------------
# CORE ANALYSIS FUNCTIONS (PURE)
# ------------------------------------------------------------------------------
def count_characters(text: str, include_spaces: bool = True) -> int:
    """Count characters in text.

    Args:
        text: Input text.
        include_spaces: When False, whitespace characters are excluded.

    Returns:
        The number of characters.
    """
    if include_spaces:
        return len(text)
    return sum(1 for ch in text if not ch.isspace())


def count_words(text: str) -> int:
    """Count words using the documented tokenisation rules."""
    return len(tokenize(text))


def count_sentences(text: str) -> int:
    """Count sentences using the documented sentence-boundary rules."""
    if not text.strip():
        return 0
    parts = SENTENCE_BOUNDARY.split(text)
    return sum(1 for part in parts if part.strip())


def word_frequencies(text: str) -> Counter[str]:
    """Return a Counter mapping each normalised word to its frequency."""
    return Counter(tokenize(text))


def most_common_word(frequencies: Counter[str]) -> tuple[str, int] | None:
    """Return the most frequent word, breaking ties alphabetically.

    Args:
        frequencies: Mapping of word to count.

    Returns:
        A (word, count) tuple, or None when the mapping is empty.
    """
    if not frequencies:
        return None
    # Sort by count descending, then word ascending for a deterministic result.
    return sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))[0]


def top_n_words(text: str, n: int = 3) -> list[tuple[str, int]]:
    """Return the n most frequent words as (word, count) tuples."""
    frequencies = word_frequencies(text)
    ranked = sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]


def count_vowels_and_consonants(text: str) -> tuple[int, int]:
    """Return (vowels, consonants), counting letters only.

    Non-letter characters are ignored. 'y' is treated as a consonant.
    """
    vowels = consonants = 0
    for ch in text.casefold():
        if ch in VOWELS:
            vowels += 1
        elif ch.isalpha():
            consonants += 1
    return vowels, consonants


def contains_word(text: str, word: str) -> bool:
    """Return True if word appears as a whole token (case-insensitive)."""
    return word.casefold() in set(tokenize(text))


def average_word_length(text: str) -> float:
    """Return the mean length of tokens, or 0.0 for empty text."""
    words = tokenize(text)
    if not words:
        return 0.0
    return sum(len(word) for word in words) / len(words)


# ------------------------------------------------------------------------------
# REPORTING (PURE: BUILD A STRING, DO NOT PRINT)
# ------------------------------------------------------------------------------
def build_report(text: str, search_word: str = "python") -> str:
    """Build a formatted analysis report.

    Args:
        text: The paragraph to analyse.
        search_word: Word to look up in the text.

    Returns:
        A multi-line report string.
    """
    cleaned = normalize_whitespace(text)
    frequencies = word_frequencies(cleaned)
    frequent = most_common_word(frequencies)
    vowels, consonants = count_vowels_and_consonants(cleaned)

    def row(label: str, value: object) -> str:
        """Format one aligned report row."""
        return f"{label:<27}: {value}"

    lines = [
        "=" * 52,
        "TEXT ANALYSIS REPORT",
        "=" * 52,
        row("Characters (with spaces)", count_characters(cleaned, True)),
        row("Characters (no spaces)", count_characters(cleaned, False)),
        row("Words", count_words(cleaned)),
        row("Sentences", count_sentences(cleaned)),
        row("Average word length", f"{average_word_length(cleaned):.2f}"),
        row("Vowels / Consonants", f"{vowels} / {consonants}"),
    ]

    if frequent is None:
        lines.append(row("Most frequent word", "(no words)"))
    else:
        word, count = frequent
        lines.append(row("Most frequent word", f"'{word}' ({count}x)"))

    lines.append(row(f"Contains '{search_word}'", contains_word(cleaned, search_word)))

    top = top_n_words(cleaned, 3)
    if top:
        formatted = ", ".join(f"{word} ({count})" for word, count in top)
        lines.append(row("Top 3 words", formatted))

    lines.append("=" * 52)
    return "\n".join(lines)


# ------------------------------------------------------------------------------
# I/O LAYER
# ------------------------------------------------------------------------------
SAMPLE_TEXT = (
    "Python is readable and powerful. Python is fun! "
    "Do you enjoy Python? It is a great first language, and practice makes "
    "you better. Keep writing small functions and testing them."
)


def main() -> None:
    """Run the text analyser interactively, falling back to sample text."""
    print("TEXT ANALYSER - paste a paragraph, or press Enter for the sample.\n")
    try:
        user_text = input("Paragraph: ").strip()
    except EOFError:
        user_text = ""

    text = user_text or SAMPLE_TEXT
    if not user_text:
        print("\n(Using sample text.)\n")

    search_word = "python"
    print(build_report(text, search_word))


if __name__ == "__main__":
    main()


# ------------------------------------------------------------------------------
# OPTIONAL CHALLENGE (IMPLEMENTED)
# ------------------------------------------------------------------------------
# "Add a text-cleaning function that normalises case and punctuation before
#  word-frequency analysis."
#
# tokenize() already does this: it collapses whitespace, trims edge
# punctuation, and casefolds. word_frequencies() therefore counts "Python",
# "python," and "PYTHON!" as the same word.
#
# Extension ideas for further practice:
#   * Exclude stop words (the, a, is, ...) before frequency analysis.
#   * Report the longest word and the longest sentence.
#   * Read from a file path instead of stdin.
#   * Add a --json mode that returns the report as a dict.
#   * Write unit tests with pytest for edge cases: empty string, punctuation
#     only, one word, one sentence with no terminator.
# ================================================================================
