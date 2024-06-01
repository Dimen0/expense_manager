import json

class BudgetManager:
    def __init__(self, budget_file='budget.json'):
        self.budget_file = budget_file
        self.budget = self.load_budget()

    def load_budget(self):
        try:
            with open(self.budget_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_budget(self):
        with open(self.budget_file, 'w') as file:
            json.dump(self.budget, file, indent=4)

    def set_budget(self, month, amount):
        self.budget[month] = amount
        self.save_budget()

    def get_budget_status(self, month, expenses):
        total_expenses = sum(expense['amount'] for expense in expenses if expense['date'].startswith(month))
        budget = self.budget.get(month, 0)
        return budget, total_expenses

    def calculate_budget_status(self, budget, total_expenses):
        remaining_budget = budget - total_expenses
        return remaining_budget

