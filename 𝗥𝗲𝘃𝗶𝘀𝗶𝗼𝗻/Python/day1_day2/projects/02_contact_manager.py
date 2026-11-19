"""
================================================================================
PROJECT 2 — Contact Manager
Concepts used (Day 1 + Day 2): dictionaries, lists, loops, conditionals,
membership operators, truthiness, break/continue, type conversion, references.
A contact = dict; the agenda = dict of name -> contact.
================================================================================
"""

class ContactManager:
    def __init__(self):
        # agenda: {name: {"phone": str, "email": str}}
        self.agenda = {}

    def add_contact(self, name, phone, email):
        if name in self.agenda:
            return False, f"Contact '{name}' already exists."
        self.agenda[name] = {"phone": phone, "email": email}
        return True, f"Contact '{name}' added."

    def search_contact(self, name):
        # .get() avoids KeyError — returns None if missing
        return self.agenda.get(name)

    def delete_contact(self, name):
        if name not in self.agenda:
            return False, f"Contact '{name}' not found."
        del self.agenda[name]
        return True, f"Contact '{name}' deleted."

    def list_contacts(self):
        if not self.agenda:          # truthiness of empty dict
            return "No contacts saved."
        lines = ["--- Contact List ---"]
        for name, info in self.agenda.items():   # dict iteration
            lines.append(f"{name}: {info['phone']}, {info['email']}")
        return "\n".join(lines)


def main():
    cm = ContactManager()

    while True:
        print("\n1. Add contact\n2. Search contact\n3. Delete contact\n4. List all\n5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            email = input("Email: ").strip()
            ok, msg = cm.add_contact(name, phone, email)
            print(msg)

        elif choice == "2":
            name = input("Name to search: ").strip()
            result = cm.search_contact(name)
            if result:
                print(f"Found -> {name}: {result}")
            else:
                print(f"Not found: {name}")

        elif choice == "3":
            name = input("Name to delete: ").strip()
            ok, msg = cm.delete_contact(name)
            print(msg)

        elif choice == "4":
            print(cm.list_contacts())

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")
            continue


if __name__ == "__main__":
    main()
