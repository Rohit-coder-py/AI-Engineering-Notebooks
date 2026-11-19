"""
================================================================================
PROJECT 3 — Grade Calculator
Concepts used (Day 2): lists, loops, conditionals, enumerate, zip, truthiness,
list methods (append, sum, len), type conversion (int/float), break/continue.
================================================================================
"""

def letter_grade(average):
    """Return letter grade based on average score."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def get_valid_score(subject):
    """Keep prompting until a valid score (0-100) is entered."""
    while True:
        raw = input(f"Enter score for {subject} (0-100): ").strip()
        try:
            score = float(raw)
        except ValueError:
            print("Please enter a numeric value.")
            continue

        if 0 <= score <= 100:
            return score
        print("Score must be between 0 and 100.")


def main():
    print("=== Grade Calculator ===")
    subjects = ["Math", "Physics", "Chemistry", "English", "Computer Science"]
    scores = []

    for subject in subjects:
        score = get_valid_score(subject)
        scores.append(score)

    total = sum(scores)
    average = total / len(scores)
    grade = letter_grade(average)

    print("\n--- Result ---")
    for subject, score in zip(subjects, scores):      # parallel iteration
        status = "Pass" if score >= 40 else "Fail"
        print(f"{subject:<20} {score:>6.2f}  [{status}]")

    print(f"{'Total':<20} {total:>6.2f}")
    print(f"{'Average':<20} {average:>6.2f}")
    print(f"{'Grade':<20} {grade}")

    # Practical loop-else pattern: check if any subject failed
    for score in scores:
        if score < 40:
            print("\nNote: At least one subject is below 40 (Fail).")
            break
    else:
        print("\nCongratulations — all subjects passed!")


if __name__ == "__main__":
    main()
