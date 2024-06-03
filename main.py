from expense_manager import ExpenseManager, CATEGORIES
from budget import BudgetManager
from income import IncomeManager
from datetime import datetime

def input_date(prompt):
    while True:
        date_input = input(f"{prompt} (YYYY-MM-DD) lub naciśnij Enter dla dzisiejszej daty: ")
        if not date_input:
            return datetime.today().strftime('%Y-%m-%d')
        elif ExpenseManager().validate_date(date_input):
            return date_input
        else:
            print("Nieprawidłowa data. Spróbuj ponownie.")

def input_amount(prompt, allow_empty=False):
    while True:
        user_input = input(prompt)
        if allow_empty and user_input == '':
            return None
        try:
            amount = float(user_input)
            return round(amount, 2)
        except ValueError:
            print("Nieprawidłowa kwota. Proszę wprowadzić wartość numeryczną.")

def input_month(prompt):
    month_input = input(f"{prompt} (YYYY-MM) lub naciśnij Enter dla bieżącego miesiąca: ")
    if not month_input:
        return datetime.today().strftime('%Y-%m')
    return month_input

def main():
    expense_manager = ExpenseManager()
    budget_manager = BudgetManager()
    income_manager = IncomeManager()

    while True:
        print("Budget manager on the Budget")
        print("==============================================")
        print("1. Wydatki")
        print("2. Budżet i przychody")
        print("3. Sprawdź status budżetu")
        print("4. Wyświetl rozkład wydatków")
        print("5. Wyjście")
        choice = input("Wybierz opcję: ")

        if choice == '1':
            expenses_menu(expense_manager, budget_manager)
        elif choice == '2':
            budget_and_income_menu(budget_manager, income_manager, expense_manager)
        elif choice == '3':
            check_budget_status(budget_manager, expense_manager, income_manager)
        elif choice == '4':
            display_expense_distribution(budget_manager, expense_manager)
        elif choice == '5':
            break
        else:
            print("Nieprawidłowa opcja, spróbuj ponownie.")

def expenses_menu(expense_manager, budget_manager):
    while True:
        print("\nMenu Wydatki:")
        print("1. Dodaj wydatek")
        print("2. Przeglądaj wydatki")
        print("3. Edytuj wydatek")
        print("4. Usuń wydatek")
        print("5. Wyświetl rozkład wydatków")
        print("6. Cofnij do menu głównego")
        choice = input("Wybierz opcję: ")

        if choice == '1':
            amount = input_amount("Podaj kwotę: ")
            print("Wybierz kategorię:")
            for i, category in enumerate(CATEGORIES, 1):
                print(f"{i}. {category}")
            category_choice = int(input("Podaj numer kategorii: "))
            category = CATEGORIES[category_choice - 1]
            date = input_date("Podaj datę")
            description = input("Podaj opis: ")
            expense_manager.add_expense(amount, category, date, description)
        elif choice == '2':
            filters = {}
            filter_choice = input("Chcesz filtrować wyniki? (tak/nie): ")
            if filter_choice.lower() == 'tak':
                print("Filtrowanie po kategorii:")
                for i, category in enumerate(CATEGORIES, 1):
                    print(f"{i}. {category}")
                category_choice = input("Podaj numer kategorii lub naciśnij Enter, aby pominąć: ")
                if category_choice:
                    filters['category'] = CATEGORIES[int(category_choice) - 1]
                date_from = input_date("Podaj datę od") if input("Podaj datę od? (tak/nie): ").lower() == 'tak' else None
                if date_from:
                    filters['date_from'] = date_from
                date_to = input_date("Podaj datę do") if input("Podaj datę do? (tak/nie): ").lower() == 'tak' else None
                if date_to:
                    filters['date_to'] = date_to
                amount_from = input_amount("Podaj minimalną kwotę lub naciśnij Enter, aby pominąć: ", allow_empty=True)
                if amount_from is not None:
                    filters['amount_from'] = amount_from
                amount_to = input_amount("Podaj maksymalną kwotę lub naciśnij Enter, aby pominąć: ", allow_empty=True)
                if amount_to is not None:
                    filters['amount_to'] = amount_to
            sort_by = input("Podaj kryterium sortowania (category/date/amount) lub naciśnij Enter, aby pominąć: ")
            expenses = expense_manager.list_expenses(filters, sort_by if sort_by else None)
            expense_manager.print_expenses(expenses)
        elif choice == '3':
            expense_id = input("Podaj ID wydatku do edycji: ")
            amount = input_amount("Podaj nową kwotę (pozostaw puste, aby nie zmieniać): ", allow_empty=True)
            print("Wybierz nową kategorię (pozostaw puste, aby nie zmieniać):")
            for i, category in enumerate(CATEGORIES, 1):
                print(f"{i}. {category}")
            category_choice = input("Podaj numer kategorii lub naciśnij Enter, aby pominąć: ")
            category = CATEGORIES[int(category_choice) - 1] if category_choice else None
            date = input_date("Podaj nową datę") if input("Zmienić datę? (tak/nie): ").lower() == 'tak' else None
            description = input("Podaj nowy opis (pozostaw puste, aby nie zmieniać): ")
            try:
                expense_manager.edit_expense(
                    expense_id,
                    amount=amount,
                    category=category if category else None,
                    date=date if date else None,
                    description=description if description else None
                )
            except ValueError as e:
                print(e)
            expenses = expense_manager.list_expenses()
            expense_manager.print_expenses(expenses)
        elif choice == '4':
            delete_choice = input("Usunąć wydatek po ID (1) czy wyszukać po opisie (2)?: ")
            if delete_choice == '1':
                expense_id = input("Podaj ID wydatku do usunięcia: ")
                expense_manager.delete_expense(expense_id)
            elif delete_choice == '2':
                description = input("Podaj opis do wyszukania: ")
                expenses = expense_manager.find_expense_by_description(description)
                expense_manager.print_expenses(expenses)
                if expenses:
                    expense_id = input("Podaj ID wydatku do usunięcia: ")
                    expense_manager.delete_expense(expense_id)
            expenses = expense_manager.list_expenses()
            expense_manager.print_expenses(expenses)
        elif choice == '5':
            month = input_month("Podaj miesiąc")
            budget, total_expenses = budget_manager.get_budget_status(month, expense_manager.expenses)
            expense_manager.display_expense_distribution(budget, total_expenses)
        elif choice == '6':
            break
        else:
            print("Nieprawidłowa opcja, spróbuj ponownie.")

def budget_and_income_menu(budget_manager, income_manager, expense_manager):
    while True:
        print("\nMenu Budżet i przychody:")
        print("1. Ustaw budżet miesięczny")
        print("2. Sprawdź status budżetu")
        print("3. Dodaj przychód")
        print("4. Wyświetl przychody")
        print("5. Cofnij do menu głównego")
        choice = input("Wybierz opcję: ")

        if choice == '1':
            month = input_month("Podaj miesiąc")
            amount = input_amount("Podaj kwotę budżetu: ")
            budget_manager.set_budget(month, amount)
        elif choice == '2':
            check_budget_status(budget_manager, expense_manager, income_manager)
        elif choice == '3':
            amount = input_amount("Podaj kwotę przychodu: ")
            source = input("Podaj źródło przychodu: ")
            date = input_date("Podaj datę przychodu")
            income_manager.add_income(amount, source, date)
        elif choice == '4':
            incomes = income_manager.list_incomes()
            print("Lista przychodów:")
            for income in incomes:
                print(f"Kwota: {income['amount']:.2f} PLN, Źródło: {income['source']}, Data: {income['date']}")
        elif choice == '5':
            break
        else:
            print("Nieprawidłowa opcja, spróbuj ponownie.")

def check_budget_status(budget_manager, expense_manager, income_manager):
    month = input_month("Podaj miesiąc")
    budget, total_expenses = budget_manager.get_budget_status(month, expense_manager.expenses)
    total_expenses_all_months = sum(expense['amount'] for expense in expense_manager.expenses)
    print(f"Budżet: {budget:.2f} PLN, Wydatki w wybranym miesiącu: {total_expenses:.2f} PLN, Wydatki całkowite: {total_expenses_all_months:.2f} PLN, Pozostało: {budget - total_expenses:.2f} PLN")
    forecasted_balance, total_income, total_expenses, forecasted_expenses = income_manager.calculate_yearly_forecast(expense_manager.expenses)
    print(f"\nRoczny przychód: {total_income:.2f} PLN")
    print(f"Prognozowane wydatki roczne: {forecasted_expenses:.2f} PLN")
    print(f"Prognozowany bilans na koniec roku: {forecasted_balance:.2f} PLN")
    if forecasted_balance > 0:
        print("Prognoza: Jesteś na plusie. Świetnie zarządzasz swoim budżetem!")
    elif forecasted_balance == 0:
        print("Prognoza: Jesteś na zero. Uważaj na swoje wydatki.")
    else:
        print("Prognoza: Jesteś na minusie. Musisz zacząć oszczędzać!")

def display_expense_distribution(budget_manager, expense_manager):
    month = input_month("Podaj miesiąc")
    budget, total_expenses = budget_manager.get_budget_status(month, expense_manager.expenses)
    expense_manager.display_expense_distribution(budget, total_expenses)

if __name__ == "__main__":
    main()
