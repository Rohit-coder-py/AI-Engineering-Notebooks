"""
PROJECT 4 (SOLVED) - Word Frequency & Text Analyzer
Concepts: strings, dict counting, sets (stop words, unique words), sorting by
value, list comprehension, tuples, slicing, loops.
Runs non-interactively with sample text.
"""
import string

TEXT = """
Python is simple. Python is powerful, and Python is popular!
Learning Python deeply means understanding variables, loops, lists, dictionaries,
and sets. Practice daily and the concepts will stay with you.
"""

STOP_WORDS = {"is", "and", "the", "will", "with", "you", "a", "of", "to", "in", "means"}


def clean_words(text):
    table = str.maketrans("", "", string.punctuation)
    return text.lower().translate(table).split()


def word_frequency(words, skip=frozenset()):
    freq = {}
    for w in words:
        if w in skip:
            continue
        freq[w] = freq.get(w, 0) + 1
    return freq


def top_n(freq, n=5):
    # sort by count desc, then alphabetically for ties
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def sentence_stats(text):
    sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    lengths = [len(s.split()) for s in sentences]
    return len(sentences), (sum(lengths) / len(lengths) if lengths else 0)


def main():
    words = clean_words(TEXT)
    freq = word_frequency(words, STOP_WORDS)
    print("Total words      :", len(words))
    print("Unique words     :", len(set(words)))
    print("Longest word     :", max(words, key=len))
    n_sent, avg_len = sentence_stats(TEXT)
    print(f"Sentences        : {n_sent} (avg {avg_len:.1f} words)")

    print("\nTop 5 words (stop words removed):")
    for word, count in top_n(freq):
        print(f"  {word:<14}{'#' * count} {count}")

    by_length = {}
    for w in set(words):
        by_length.setdefault(len(w), []).append(w)
    print("\nWords grouped by length (first 3 groups):")
    for length in sorted(by_length)[:3]:
        print(f"  {length}: {sorted(by_length[length])}")

    letters = word_frequency([c for c in TEXT.lower() if c.isalpha()])
    print("\nMost common letter:", top_n(letters, 1)[0])


if __name__ == "__main__":
    main()
