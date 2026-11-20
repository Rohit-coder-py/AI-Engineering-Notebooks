# Day 3 — Strings, Functions & Reusable Code

> **Date:** November 21, 2026
> **Roadmap:** Python Mastery — 7-Day Learning & First-Interview Roadmap
> **Core objective:** Write readable, reusable programs and understand how functions receive arguments, return values, and use scope.

This folder is the complete, runnable Day 3 study pack: guided lessons, a project, practical drills, and a full interview question bank.

---

## Folder Map

| File | Focus | Key interview topics |
|---|---|---|
| `01_string_fundamentals.py` | Creation, indexing, slicing, immutability, concatenation, all three formatting styles | `s[::-1]`, out-of-range slices, `str` vs `bytes`, `join` vs `+=` |
| `02_string_methods.py` | Case, strip, split/join, replace, find/index, count, startswith/endswith, `is*`, layout | `split()` vs `split(" ")`, `strip` char-set trap, `find` vs `index` |
| `03_advanced_strings.py` | Membership, escapes/raw strings, comparison, Unicode | `in` vs word check, `Z < a`, `==` vs `is`, encode/decode, NFC |
| `04_function_fundamentals.py` | `def`, parameters vs arguments, `return` vs `print`, multiple returns, first-class functions | Implicit `None`, tuple returns, definition vs call time |
| `05_function_arguments.py` | Positional/keyword/default, `/` and `*`, `*args`, `**kwargs`, unpacking | Mutable default trap, forwarding, signature order |
| `06_scope_legb.py` | LEGB, `global`, `nonlocal`, closures, comprehension scope | `UnboundLocalError`, late binding, built-in shadowing |
| `07_functional_tools.py` | lambda, higher-order functions, map/filter, `sorted(key=...)`, docstrings, type hints | Lazy iterators, stability, `sort` vs `sorted`, hints not enforced |
| `08_function_design.py` | Single responsibility, pure functions, side effects, globals, recursion | Mutable defaults, testability, `RecursionError`, memoisation |
| `09_day3_interview_questions.py` | 66 theory Q&A + 20 practical drills with outputs | Rapid revision before interviews |
| `10_text_analyser_project.py` | Full Text Analyser project with assumptions, docstrings, types | End-to-end design and decomposition |
| `Day3_Interview_Questions.md` | Complete interview question bank (150+ questions, answers, coding challenges, rubric) | Mock interview and active recall |

---

## How to Run

```bash
# From this folder
python 01_string_fundamentals.py
python 09_day3_interview_questions.py
python 10_text_analyser_project.py
```

The project reads one line from stdin. Press **Enter** to analyse the built-in sample text, or pipe input:

```bash
echo "Your paragraph here." | python 10_text_analyser_project.py
```

Every lesson is self-contained and prints its own annotated output.

---

## Recommended Study Order

1. **Read + run** `01` → `03` (strings).
2. **Read + run** `04` → `08` (functions, scope, tools, design).
3. **Answer aloud** using `Day3_Interview_Questions.md` (cover the answers).
4. **Run** `09_day3_interview_questions.py` and predict outputs first.
5. **Build** `10_text_analyser_project.py` yourself, then compare.
6. **Mock interview** using the 45-minute plan in the Markdown file.

Suggested time split: **60% learning/implementation, 20% project, 20% recall/revision.**

---

## Syllabus Coverage

### A. Strings

- [x] Creation and indexing
- [x] Positive and negative indexing
- [x] Slicing (including negative steps and clamping)
- [x] Immutability (hashability, interning, performance)
- [x] Concatenation and repetition
- [x] Formatting: f-strings, `format()`, `%`
- [x] `lower`, `upper`, `title`
- [x] `strip`, `split`/`join`, `replace`
- [x] `find`/`index`, `count`, `startswith`/`endswith`
- [x] Membership, escapes, raw strings, comparison
- [x] Basic Unicode awareness (code points, UTF-8, normalisation)

### B. Functions

- [x] Fundamentals, parameters vs arguments, return vs print
- [x] Positional, keyword, default arguments
- [x] Positional-only (`/`) and keyword-only (`*`)
- [x] `*args`, `**kwargs`, unpacking
- [x] Local/global scope, `global`, `nonlocal`, LEGB
- [x] lambda, higher-order functions, `map`, `filter`, `sorted(key=...)`
- [x] Docstrings and type hints

### C. Function Design

- [x] Decomposition and single responsibility
- [x] Avoiding unnecessary globals
- [x] Side effects and pure functions
- [x] Mutable default pitfalls
- [x] Recursion and base cases

### Project

- [x] Text Analyser with documented assumptions
- [x] Character, word, and sentence counts
- [x] Most frequent word, vowels/consonants
- [x] Whitespace normalisation and word lookup
- [x] Separate functions + formatted report
- [x] Optional challenge (case/punctuation normalisation)

---

## Project Assumptions (Say These in an Interview)

1. **Character** = Unicode code point; the "no spaces" count excludes whitespace.
2. **Word** = whitespace-separated token after trimming edge punctuation; internal apostrophes/hyphens stay.
3. **Sentence** = text ending in `.`, `!`, or `?`; runs of terminators count once; abbreviations are not handled.
4. **Frequency** is case-insensitive (`casefold`).
5. Input whitespace is normalised before analysis.

Stating assumptions is part of the exercise: ambiguous requirements are normal in real work.

---

## Quick Self-Check

Before Day 4, can you:

- [ ] Explain immutability and why strings are hashable?
- [ ] Predict any slice, including `s[::-1]` and out-of-range bounds?
- [ ] Explain `split()` vs `split(" ")` and `strip` vs `removeprefix`?
- [ ] Explain `==` vs `is` and `str` vs `bytes`?
- [ ] Explain parameters vs arguments and `return` vs `print`?
- [ ] Explain why `def f(x, items=[])` is dangerous and fix it?
- [ ] Use `*args`, `**kwargs`, `/`, and `*` correctly?
- [ ] Explain LEGB and fix an `UnboundLocalError`?
- [ ] Explain why lambdas in a loop capture the last value?
- [ ] Write and analyse a recursive function with a base case?
- [ ] Design a small program as pure functions plus an I/O edge?

If any answer is shaky, revisit the matching file and the question bank section before moving on.

---

## Related Files

- Master plan: `../Day_3_Python_Mastery.md`
- Day 1 and Day 2 lessons: `../../day1/`, `../../day2/`

**Day 3 is complete when you can explain, implement, and reason about these topics independently — not merely when the files have been read.**
