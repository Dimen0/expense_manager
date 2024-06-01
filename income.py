import json
from datetime import datetime

class IncomeManager:
    def __init__(self, income_file="income.json"):
        self.income_file = income_file
        self.income = self.incomes = self.load_incomes()

    def load_incomes(self):
        try:
            with open(self.income_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_incomes(self):
        with open(self.income_file, 'w') as file:
            json.dump(self.incomes, file, indent=4)

    def add_income(self, amount, source, date):
        income = {
            'amount': round(amount, 2),
            'source': source,
            'date': date
        }
        self.incomes.append(income)
        self.save_incomes()

    def list_incomes(self):
        return self.incomes


    def calculate_yearly_forecast(self, expenses):
        total_income = sum(income['amount'] for income in self.incomes)
        total_expenses = sum(expense['amount'] for expense in expenses)
        current_month = datetime.now().month
        average_monthly_expense = total_expenses / current_month
        forecasted_expenses = total_expenses + average_monthly_expense * (12 - current_month)
        forecasted_balance = total_income * 12 - forecasted_expenses
        return forecasted_balance, total_income, total_expenses, forecasted_expenses