"""
PROJECT 9 (BLANK) - To-Do List CLI (capstone for Day 1 + Day 2)
================================================================
Combine everything: variables, types, operators, conditionals, loops,
list, tuple, set, dict, functions, input validation.

DATA SHAPE (list of dicts)
    tasks = [
        {"id": 1, "title": "Revise lists", "priority": "high", "done": False,
         "tags": {"python", "study"}},
    ]

REQUIREMENTS
1. add_task(tasks, title, priority="medium", tags=())
      - priority must be one of {"low", "medium", "high"} else ValueError
      - id = max existing id + 1 (1 if empty). Strip title; reject empty.
2. complete_task(tasks, task_id)      -> True/False
3. delete_task(tasks, task_id)        -> True/False
4. list_tasks(tasks, status="all", priority=None, tag=None)
      -> filtered list. status: "all" | "pending" | "done"
5. sort_tasks(tasks)                  -> new list: pending first, then by priority
                                         (high > medium > low), then by id
6. stats(tasks)                       -> dict: total, done, pending, percent_done,
                                         per_priority counts, all_tags (sorted list)
7. print_tasks(tasks)                 -> table with [x]/[ ] marks
8. main()                             -> menu loop (1 Add, 2 Complete, 3 Delete,
                                         4 List/filter, 5 Stats, 0 Exit).
                                         Never crash on bad input.

HINTS
- priority_rank = {"high": 0, "medium": 1, "low": 2}; use as sort key
- next((t for t in tasks if t["id"] == task_id), None)
- sets make tag filtering/unions easy

BONUS
- Persist to tasks.json (json.dump / json.load; convert sets <-> lists)
- Add due dates with datetime and an 'overdue' filter
"""

VALID_PRIORITIES = {"low", "medium", "high"}
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


def add_task(tasks, title, priority="medium", tags=()):
    # TODO
    pass


def complete_task(tasks, task_id):
    # TODO
    pass


def delete_task(tasks, task_id):
    # TODO
    pass


def list_tasks(tasks, status="all", priority=None, tag=None):
    # TODO
    pass


def sort_tasks(tasks):
    # TODO
    pass


def stats(tasks):
    # TODO
    pass


def print_tasks(tasks):
    # TODO
    pass


def main():
    # TODO
    pass


if __name__ == "__main__":
    main()
    # Self-tests (uncomment when ready):
    # t = []
    # add_task(t, "Revise lists", "high", ["python"])
    # add_task(t, "Read sets", "low")
    # assert [x["id"] for x in t] == [1, 2]
    # assert complete_task(t, 1) is True and complete_task(t, 99) is False
    # assert [x["id"] for x in sort_tasks(t)] == [2, 1]
    # assert stats(t)["percent_done"] == 50.0
