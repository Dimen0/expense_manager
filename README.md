S25599 - Dawid Kamiński

# Aplikacja do Zarządzania Wydatkami

Prosta aplikacja konsolowa do zarządzania wydatkami i budżetem osobistym.

## Funkcjonalność:

Aplikacja umożliwia dodawanie, edytowanie, usuwanie, przeglądanie i przechowywanie wydatków.
Można ustawić i sprawdić:
- budżet miesięczny
- przychody (jeden lub kilka)

Oprócz tego
- wykres z wydatkami i budżetem
- sprawdzanie i weryfikacja miesięcznego oraz rocznego bilansu z krótką adnotacją
- Aplikacja poprawnie zapisuje i odczytuje dane po zamknięciu i ponownym uruchomieniu.

### Logika

- Aplikacja posiada interfejs w konsoli.
- Każdy wydatek ma unikalny identyfikator przydzielany na podstawie kategorii, kwotę, kategorię, datę oraz opis.
- Użytkownik może filtrować wydatki według kategorii, daty lub kwoty.
- Można sortować wydatki według wszystkich kryteriów (domyślnie ID).
- Dane o wydatkach, budżecie i przychodach powinny być przechowywane w plikach JSON.
- Użytkownik ma możliwość usuwania wydatków na podstawie identyfikatora lub szukając po opisie.
- Użytkownik może edytować istniejące wydatki (kwota, kategoria, data, opis). Przy zmianie kategorii aktualizowane jest ID.
- Można ustalić i wyświetlić przychody(miesięczne). 
- Można ustalić i wyświetlić budżet dla wybranego miesiąca.
- Można wyświetlić graficzną reprezentację wydatków z podziałem na kategorie

### Status budżetu

Przy wyświetlaniu statusu budżetu (dla danego miesiąca) aplikacja wyświetla:

- Budżet
- Wydatki w danym miesiącu
- Suma wydatków dla całego roku(w którym znajduje się miesiąc)
- Różnica w danym miesiącu
- Zsumowane roczne przychody
- Prognoza:
Wyświetlana jest prognoza wydatków do końca roku( **Suma wydatków do danego miesiąca** + **średnie prognozowane miesięczne wydatki** wyliczone na podstawie **suma wydatków** / **liczba miesięcy do teraz** * **pozostałe miesiące do końca roku**).

- Na podstawie prognozy wyświetlany jest komunikat lub ostrzeżenie o negatywnej prognozie.




### Obsługa błędów:

Aplikacja obsługiwać błędy, takie jak podanie nieprawidłowego ID, kwoty, daty, wybranie nieistniejącej opcji w menu.

Użytkownik otrzymuje stosowny komunikat o otrzymanym błędzie.



### To do:
Poprawa interfejsu - DONE 

Ewentualna implementacja lepszych wykresów np. plottext

## Struktura projektu

main.py - główne menu i obsługa inputów użytkownika

expense_manager.py : przechowywanie, wyświetlanie i praca na wydatkach

budget.py : logika budżetu

income.py : logika przychodów

expenses.json, budget.json, income.json - przechowywanie informacji użytkownika

Na ten moment nie ma wymaganych żadnych dodatkowych bibliotek. 








