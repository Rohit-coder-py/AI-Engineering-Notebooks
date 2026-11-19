"""
PROJECT 6 (BLANK) - Inventory Manager
======================================
Concepts to practice: dict of dicts, functions, loops, sorting, try/except,
f-string tables, comprehensions.

DATA SHAPE
    inventory = {
        "apple":  {"price": 30.0, "qty": 50},
        "banana": {"price": 10.0, "qty": 100},
    }

REQUIREMENTS (implement each function)
1. add_item(inv, name, price, qty)       -> adds new item or increases qty if it exists
                                            (update price to the new price). Reject negatives.
2. remove_item(inv, name)                -> delete item, return True/False
3. sell_item(inv, name, qty)             -> reduce qty; raise ValueError("Insufficient stock")
                                            if not enough; return the sale amount
4. low_stock(inv, threshold=10)          -> list of names with qty < threshold
5. total_value(inv)                      -> sum(price * qty)
6. report(inv)                           -> print a neat table sorted by total value (desc)
7. search(inv, text)                     -> case-insensitive partial name match, return dict
8. main(): menu-driven loop that uses all functions (handle bad input safely)

HINTS
- inv.get(name), `in` for membership, sorted(..., key=lambda kv: ...)
- f"{name:<10}{price:>8.2f}" for aligned columns

BONUS
- Keep a `sales_log` list of tuples (name, qty, amount) and print daily revenue
- Save/load inventory using the json module
"""


def add_item(inv, name, price, qty):
    # TODO
    pass


def remove_item(inv, name):
    # TODO
    pass


def sell_item(inv, name, qty):
    # TODO
    pass


def low_stock(inv, threshold=10):
    # TODO
    pass


def total_value(inv):
    # TODO
    pass


def report(inv):
    # TODO
    pass


def search(inv, text):
    # TODO
    pass


def main():
    # TODO
    pass


if __name__ == "__main__":
    main()
    # Self-tests (uncomment when ready):
    # inv = {}
    # add_item(inv, "apple", 30, 5); add_item(inv, "apple", 32, 5)
    # assert inv["apple"] == {"price": 32, "qty": 10}
    # assert sell_item(inv, "apple", 4) == 128
    # assert low_stock(inv) == ["apple"]
    # assert total_value(inv) == 32 * 6
