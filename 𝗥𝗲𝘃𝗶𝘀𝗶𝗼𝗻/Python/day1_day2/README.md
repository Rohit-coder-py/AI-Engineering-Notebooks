# Day 1 + Day 2: Python Revision Kit (Interview Focused)

Goal: deepen fundamentals, not tick boxes. Each file = **theory in comments + runnable practical code + "predict the output" checks**.

## Study order

| # | File | Topics |
|---|------|--------|
| 01 | `01_variables.py` | assignment, reassignment, internals (names → objects), naming, dynamic typing, multiple assignment, references, `is` vs `==`, copying |
| 02 | `02_data_types.py` | int/float/complex/bool/str/None, mutable vs immutable, truthiness, float precision, string methods |
| 03 | `03_type_conversion.py` | implicit vs explicit, int/float/str/bool, base conversion, container conversion, safe parsing |
| 04 | `04_operators.py` | arithmetic, comparison, logical (short-circuit), bitwise, identity/membership, precedence, walrus |
| 05 | `05_conditionals.py` | if/elif/else, nested, guard clauses, ternary, match-case |
| 06 | `06_loops.py` | for/while, range, enumerate/zip, break/continue/pass, loop-else, nested, comprehensions, pitfalls |
| 07 | `07_lists.py` | indexing/slicing, methods, sorting, copying, nested, complexity |
| 08 | `08_tuples.py` | immutability, packing/unpacking, hashability, namedtuple |
| 09 | `09_sets.py` | uniqueness, set algebra, frozenset, performance |
| 10 | `10_dictionaries.py` | access, methods, views, comprehension, defaultdict/Counter, patterns |
| 11 | `11_interview_theory.md` | 75 theory Q&A + rapid-fire table |
| 12 | `12_interview_practical_solved.py` | 18 predict-output + 30 coding questions with solutions and tests |
| 13 | `13_interview_practice_BLANK.py` | 20 coding questions for YOU to solve (auto-tested) |
| - | `projects/` | 4 solved mini-projects + 5 blank ones |

## How to study (suggested ~1 day each)

1. **Read** a file top to bottom. Before each `print`, guess the output.
2. **Run** it: `python 01_variables.py`. Compare with your guess; investigate every surprise.
3. **Break it**: change values, trigger the errors on purpose.
4. After a topic, answer the matching questions in `11_interview_theory.md` out loud (no notes).
5. End of each day: solve from `13_interview_practice_BLANK.py`, then `projects/` blanks.

## Requirements
Python 3.10+ (uses `match-case` and `|` for dicts). Check with `python --version`.

## The Day-2 end-of-day checklist
- [ ] I can explain why `a = b = []` is dangerous
- [ ] I can explain `is` vs `==` with an example
- [ ] I know mutable vs immutable and can name 5 of each
- [ ] I can state the complexity of list/set/dict operations
- [ ] I solved 15+/20 of the BLANK interview problems
- [ ] I finished at least 2 BLANK projects without looking at solved ones
