"""
PROJECT 3 (SOLVED) - Student Grade Calculator & Report
Concepts: dict of lists, tuples, sorting with key, loops, conditionals,
comprehensions, min/max/sum, formatted output.
Runs non-interactively with sample data.
"""

STUDENTS = {
    "Asha": {"Math": 92, "Science": 88, "English": 79},
    "Ravi": {"Math": 67, "Science": 74, "English": 81},
    "Neha": {"Math": 45, "Science": 52, "English": 60},
    "Karan": {"Math": 98, "Science": 95, "English": 91},
}


def grade_for(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    return "F"


def student_summary(marks):
    """Return (total, average, grade) as a tuple."""
    total = sum(marks.values())
    avg = total / len(marks)
    return total, avg, grade_for(avg)


def subject_stats(students):
    """Per-subject average, topper and lowest."""
    subjects = next(iter(students.values())).keys()
    stats = {}
    for sub in subjects:
        scores = {name: marks[sub] for name, marks in students.items()}
        stats[sub] = {
            "avg": sum(scores.values()) / len(scores),
            "topper": max(scores, key=scores.get),
            "lowest": min(scores, key=scores.get),
        }
    return stats


def main():
    print(f"{'Name':<8}{'Total':>7}{'Avg':>8}  Grade")
    print("-" * 30)
    summaries = {n: student_summary(m) for n, m in STUDENTS.items()}
    ranked = sorted(summaries.items(), key=lambda kv: kv[1][1], reverse=True)
    for rank, (name, (total, avg, grade)) in enumerate(ranked, start=1):
        print(f"{name:<8}{total:>7}{avg:>8.2f}  {grade}   (#{rank})")

    print("\nSubject statistics")
    for sub, s in subject_stats(STUDENTS).items():
        print(f"  {sub:<8} avg={s['avg']:.1f} topper={s['topper']} lowest={s['lowest']}")

    failing = [n for n, (_, avg, _) in summaries.items() if avg < 50]
    distinction = [n for n, (_, avg, _) in summaries.items() if avg >= 85]
    print("\nDistinction:", distinction or "none")
    print("Needs support:", failing or "none")

    class_avg = sum(avg for _, avg, _ in summaries.values()) / len(summaries)
    print(f"Class average: {class_avg:.2f}")


if __name__ == "__main__":
    main()
