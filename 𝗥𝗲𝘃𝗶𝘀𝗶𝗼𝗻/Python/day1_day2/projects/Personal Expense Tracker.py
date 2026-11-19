# Core requirements
# 1. Add an expense.
# 2. View all expenses.
# 3. Calculate total expenses.
# 4. Calculate average expenses.
# 5. Find the highest and lowest expense.
# 6. Filter expenses by category.
# 7. Delete an expense.
# 8. Display unique categories.
# 9. Validate user input.
# 10. Exit the application.
menu = """
========================================
       PERSONAL EXPENSE TRACKER
========================================

1. Add Expense
2. View All Expenses
3. Calculate Total Expenses
4. Calculate Average Expense
5. Find Highest Expense
6. Find Lowest Expense
7. Filter Expenses by Category
8. Delete Expense
9. View Unique Categories
10. Exit

========================================
"""

expenses = []

while True:
    print(menu)
    print("\n")

    choose = input("Enter your choice :(Enter 'exit' to quit) ").strip()

    if choose.strip().lower() == "exit":
        print("Thanks for visiting the website")
        break

    else:
        print("\n")
        if choose == "1":
            print("\n========== ADD EXPENSE ==========")
            amount = int(input("Enter your expense amount :"))
            category = input("Enter your expense category")
            description = input("Enter description :")

            expense = {
                "amount": amount,
                "category": category,
                "description": description,
            }

            expenses.append(expense)
            print(f"\nYour expense of amount ₹{amount} added sucessfully")
            print(f"To view your expense press '2'")

        elif choose == "2":
            print("\n========== ALL EXPENSES ==========")

            if not expenses:
                print("No expenses found!")

            else:
                for index, expense in enumerate(expenses, start=1):
                    print(f"\nExpense #{index}")
                    print("-" * 30)
                    print(f"Amount      : ₹{expense['amount']}")
                    print(f"Category    : {expense['category']}")
                    print(f"Description : {expense['description']}")

                print("\nAll expenses displayed successfully!")

        elif choose == "3":
            print("The total of all your expenses is:")

            exp_total = 0

            for expense in expenses:
                exp_total = exp_total + expense["amount"]

            print(f"Total Expenses: ₹{exp_total}")
