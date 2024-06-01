import json
from datetime import datetime

CATEGORIES = [
    "Jedzenie", "Mieszkanie", "Inne opłaty i rachunki",
    "Zdrowie, higiena i chemia", "Ubrania i obuwie",
    "Relaks", "Transport", "Inne wydatki"
]

class ExpenseManager:
    def __init__(self, data_file='expenses.json'):
        self.data_file = data_file
        self.expenses = self.load_expenses()

    def load_expenses(self):
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_expenses(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def get_next_id(self, category):
        category_expenses = [expense for expense in self.expenses if expense['category'] == category]
        return f"{category[0]}-{len(category_expenses) + 1}"

    def update_ids(self):
        for category in CATEGORIES:
            category_expenses = [expense for expense in self.expenses if expense['category'] == category]
            for i, expense in enumerate(category_expenses, 1):
                expense['id'] = f"{category[0]}-{i}"

    def add_expense(self, amount, category, date, description):
        amount = round(amount, 2)
        expense_id = self.get_next_id(category)
        expense = {
            'id': expense_id,
            'amount': amount,
            'category': category,
            'date': date,
            'description': description
        }
        self.expenses.append(expense)
        self.update_ids()
        self.save_expenses()

    def list_expenses(self, filters=None, sort_by=None):
        expenses = self.expenses
        if filters:
            if 'category' in filters:
                expenses = [expense for expense in expenses if expense['category'] == filters['category']]
            if 'date_from' in filters:
                expenses = [expense for expense in expenses if expense['date'] >= filters['date_from']]
            if 'date_to' in filters:
                expenses = [expense for expense in expenses if expense['date'] <= filters['date_to']]
            if 'amount_from' in filters:
                expenses = [expense for expense in expenses if expense['amount'] >= filters['amount_from']]
            if 'amount_to' in filters:
                expenses = [expense for expense in expenses if expense['amount'] <= filters['amount_to']]
        if sort_by:
            expenses.sort(key=lambda x: x[sort_by])
        else:
            expenses.sort(key=lambda x: x['id'])
        return expenses

    def print_expenses(self, expenses):
        if not expenses:
            print("Nie znaleziono wyników.")
        for expense in expenses:
            print(f"ID: {expense['id']}, Kwota: {expense['amount']:.2f} PLN, Kategoria: {expense['category']}, Data: {expense['date']}, Opis: {expense['description']}")
    def edit_expense(self, expense_id, amount=None, category=None, date=None, description=None):
        for expense in self.expenses:
            if expense['id'] == expense_id:
                if amount is not None:
                    expense['amount'] = round(amount, 2)
                if category is not None and expense['category'] != category:
                    expense['category'] = category
                    expense['id'] = self.get_next_id(category)
                if date is not None:
                    expense['date'] = date
                if description is not None:
                    expense['description'] = description
                self.update_ids()
                self.save_expenses()
                return
        raise ValueError(f'Expense with id {expense_id} not found.')

    def delete_expense(self, expense_id):
        initial_length = len(self.expenses)
        self.expenses = [expense for expense in self.expenses if expense['id'] != expense_id]
        if len(self.expenses) == initial_length:
            print(f"Wydatek o ID {expense_id} nie istnieje.")
        else:
            print("Usunieto")
            self.update_ids()
            self.save_expenses()

    def find_expense_by_description(self, description):
        return [expense for expense in self.expenses if description.lower() in expense['description'].lower()]

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def display_expense_distribution(self, budget, total_expenses):
        from collections import defaultdict
        category_totals = defaultdict(float)
        for expense in self.expenses:
            category_totals[expense['category']] += expense['amount']

        max_length = max(len(category) for category in category_totals)
        max_expense = max(category_totals.values())
        bar_scale = max_expense if max_expense > budget else budget

        for category, total in category_totals.items():
            bar_length = int(total / bar_scale * 50)
            print(f"{category.ljust(max_length)} | {'#' * bar_length} {total:.2f} PLN")

        budget_line = int(budget / bar_scale * 50)
        print(f"\n{'Budżet'.ljust(max_length)} | {'-' * budget_line} {budget:.2f} PLN")

        print("\nWydatki całkowite: {:.2f} PLN".format(total_expenses))
        if total_expenses > budget:
            print("Przekroczono budżet o {:.2f} PLN".format(total_expenses - budget))
        else:
            print("Pozostało w budżecie: {:.2f} PLN".format(budget - total_expenses))

