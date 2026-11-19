"""
PROJECT 2 (SOLVED) - Contact Book (CLI)
Concepts: dict (nested), list, set, loops, functions, string methods,
sorting, input validation, try/except, f-strings.
"""


def validate_phone(phone):
    digits = phone.replace(" ", "").replace("-", "")
    return digits.isdigit() and len(digits) == 10


def add_contact(book):
    name = input("Name: ").strip().title()
    if not name:
        print("Name can't be empty.")
        return
    if name in book:
        print(f"{name} already exists. Use update instead.")
        return
    phone = input("Phone (10 digits): ").strip()
    if not validate_phone(phone):
        print("Invalid phone number.")
        return
    email = input("Email (optional): ").strip().lower()
    tags = {t.strip().lower() for t in input("Tags (comma separated, optional): ").split(",") if t.strip()}
    book[name] = {"phone": phone, "email": email, "tags": tags}
    print(f"Added {name}.")


def search(book):
    query = input("Search (name/phone/tag): ").strip().lower()
    found = {
        n: d for n, d in book.items()
        if query in n.lower() or query in d["phone"] or query in d["tags"]
    }
    show(found)


def update_contact(book):
    name = input("Name to update: ").strip().title()
    if name not in book:
        print("Not found.")
        return
    phone = input(f"New phone [{book[name]['phone']}]: ").strip()
    if phone:
        if not validate_phone(phone):
            print("Invalid phone, keeping old.")
        else:
            book[name]["phone"] = phone
    email = input(f"New email [{book[name]['email']}]: ").strip().lower()
    if email:
        book[name]["email"] = email
    print("Updated.")


def delete_contact(book):
    name = input("Name to delete: ").strip().title()
    if book.pop(name, None) is None:
        print("Not found.")
    else:
        print(f"Deleted {name}.")


def show(book):
    if not book:
        print("(no contacts)")
        return
    print(f"\n{'Name':<15}{'Phone':<14}{'Email':<24}Tags")
    print("-" * 62)
    for name in sorted(book):
        d = book[name]
        print(f"{name:<15}{d['phone']:<14}{d['email']:<24}{', '.join(sorted(d['tags']))}")
    print(f"Total: {len(book)}")


def main():
    book = {
        "Asha": {"phone": "9876543210", "email": "asha@example.com", "tags": {"friend"}},
    }
    menu = {"1": ("Add", add_contact), "2": ("Search", search), "3": ("Update", update_contact),
            "4": ("Delete", delete_contact), "5": ("Show all", show)}
    while True:
        print("\n=== CONTACT BOOK ===")
        for key, (label, _) in menu.items():
            print(f"{key}. {label}")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Bye!")
            break
        if choice in menu:
            func = menu[choice][1]
            func(book)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
