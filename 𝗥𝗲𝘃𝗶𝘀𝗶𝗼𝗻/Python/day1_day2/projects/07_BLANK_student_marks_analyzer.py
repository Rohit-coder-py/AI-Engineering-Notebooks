"""
PROJECT 7 (BLANK) - Marks Analyzer (list / tuple / set practice)
=================================================================
Given the raw data below, write the functions. No pandas, no statistics module.

RAW = list of tuples: (roll_no, name, [marks in 5 subjects])

REQUIREMENTS
1. average(marks)                   -> float rounded to 2 decimals
2. topper(data)                     -> (name, avg) of the best student
3. rank_list(data)                  -> list of (rank, name, avg), highest first,
                                       ties share the same rank (1, 2, 2, 4 ...)
4. median(nums)                     -> without statistics module
5. subject_toppers(data)            -> dict {subject_index: name_of_topper}
6. students_above_average(data)     -> set of names scoring above class average
7. unique_scores(data)              -> sorted list of all distinct marks seen
8. grade_distribution(data)         -> dict {"A": n, "B": n, ...}
                                       (A>=85, B>=70, C>=55, else D based on average)
9. normalize(marks)                 -> list scaled to 0-100 using min-max of that list
10. print_report(data)              -> aligned table with all the above

HINTS
- sorted(..., key=lambda s: s[1], reverse=True)
- zip(*marks_lists) transposes subjects
- set comprehension for students_above_average

BONUS
- Detect students whose marks are strictly increasing across subjects
- Find the most "consistent" student (lowest max-min spread)
"""

RAW = [
    (1, "Asha", [92, 88, 79, 95, 85]),
    (2, "Ravi", [67, 74, 81, 60, 72]),
    (3, "Neha", [45, 52, 60, 48, 55]),
    (4, "Karan", [98, 95, 91, 99, 94]),
    (5, "Meera", [67, 74, 81, 60, 72]),
]
SUBJECTS = ["Math", "Science", "English", "CS", "Hindi"]


def average(marks):
    # TODO
    pass


def topper(data):
    # TODO
    pass


def rank_list(data):
    # TODO
    pass


def median(nums):
    # TODO
    pass


def subject_toppers(data):
    # TODO
    pass


def students_above_average(data):
    # TODO
    pass


def unique_scores(data):
    # TODO
    pass


def grade_distribution(data):
    # TODO
    pass


def normalize(marks):
    # TODO
    pass


def print_report(data):
    # TODO
    pass


if __name__ == "__main__":
    print_report(RAW)
    # Self-tests (uncomment when ready):
    # assert average([90, 80, 70]) == 80.0
    # assert topper(RAW)[0] == "Karan"
    # assert median([5, 1, 3]) == 3 and median([4, 1, 3, 2]) == 2.5
    # assert rank_list(RAW)[2][0] == rank_list(RAW)[3][0]     # Ravi & Meera tie
    # assert normalize([10, 20, 30]) == [0.0, 50.0, 100.0]
