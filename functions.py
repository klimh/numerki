import math
from math import *


def choose_function():
    print('Podaj numer wybranej funkcji:')
    print(" 1. Wielomian \n 2. Trygonometryczna \n 3. Wykładnicza \n 4. Złożenie funkcji")

    choice = None
    while choice is None:
        choice = input("Wybierz numer funkcji (1-4): ")
        if choice == "1":
            return polynomial_choose()
        elif choice == "2":
            return trigonometric_choose()
        elif choice == "3":
            return exponential_choose()
        elif choice == "4":
            return composite_choose()
        else:
            print("Wybrano zły numer funkcji.")
            choice = None


def polynomial_choose():
    """Pobiera od użytkownika współczynniki wielomianu i zwraca funkcję obliczającą jego wartość według schematu Hornera."""
    print("Wybrano funkcję wielomianową.\n")

    degree = None
    while degree is None or degree < 0:
        try:
            degree = int(input("Podaj stopień wielomianu (dodatnia liczba całkowita): "))
            if degree < 0:
                print("Błąd: stopień musi być dodatnią liczbą całkowitą.")
        except ValueError:
            print("Błąd: niepoprawna wartość, podaj liczbę całkowitą.")
    coefficents = []

    for i in range(degree, -1, -1):
        coe = None
        while coe is None:
            try:
                coe = float(input(f"Podaj współczynnik przy x^{i}: "))
                coefficents.append(coe)
            except ValueError:
                print("Błąd: niepoprawna wartość, podaj liczbę rzeczywistą.")

    def polynomial_calc(x):
        result = coefficents[0]
        for a in coefficents[1:]:
            result = result * x + a
        return result

    return polynomial_calc


def trigonometric_choose():
    """Pobiera od użytkownika parametry funkcji trygonometrycznej i zwraca funkcję obliczającą jej wartość.
    """
    print("Wybrano funkcję trygonometryczną.\n")

    n = None
    while n is None or n < 1 or n > 8:
        try:
            print("Podaj numer funkcji (1-8): ")
            print(" 1. sin(x) \n 2. cos(x) \n 3. tg(x) \n 4. arcsin(x) \n 5. arccos(x)\n 6. arctg(x)")
            n = int(input())
            if n < 1 or n > 8:
                print("Błąd: niepoprawna wartość, podaj liczbę z przedziału 1-8.")
        except ValueError:
            print("Błąd: niepoprawna wartość, podaj liczbę całkowitą.")

    if n == 1:
        fun = math.sin
    elif n == 2:
        fun = math.cos
    elif n == 3:
        fun = math.tan
    elif n == 4:
        fun = math.asin
    elif n == 5:
        fun = math.acos
    elif n == 6:
        fun = math.atan

    def trig_calc(x):
        return fun(x)

    return trig_calc


def exponential_choose():
    """Pobiera od użytkownika parametry funkcji wykładniczej i zwraca funkcję obliczającą jej wartość.

    Funkcja ma postać:
        f(x) = A * exp(B * x) + C
    """
    print("Wybrano funkcję wykładniczą w postaci f(x) = A * exp(B * x) + C.\n")

    A = None
    while A is None:
        try:
            A = float(input("Podaj wartość współczynnika A (mnożnik): "))
        except ValueError:
            print("Błąd: niepoprawna wartość, podaj liczbę rzeczywistą.")

    B = None
    while B is None:
        try:
            B = float(input("Podaj wartość współczynnika B (współczynnik wykładnika): "))
        except ValueError:
            print("Błąd: niepoprawna wartość, podaj liczbę rzeczywistą.")

    C = None
    while C is None:
        try:
            C = float(input("Podaj wartość współczynnika C (przesunięcie): "))
        except ValueError:
            print("Błąd: niepoprawna wartość, podaj liczbę rzeczywistą.")

    def expo_calc(x):
        from math import exp
        return A * exp(B * x) + C

    return expo_calc


def composite_choose():
    """Pozwala użytkownikowi wybrać liczbę funkcji do złożenia, a następnie kolejne funkcje,
    i zwraca funkcję będącą ich kompozycją (funkcja złożona).
    """
    print("Wybrano funkcję złożoną.\n Podawaj funkcje od wewnętrznej do zewnętrznej.")

    # Pobieramy liczbę funkcji do złożenia (minimum 2)
    n = None
    while n is None or n < 2:
        try:
            n = int(input("Podaj liczbę funkcji do złożenia (minimum 2): "))
        except ValueError:
            print("Błąd: niepoprawna wartość, podaj liczbę całkowitą.")

    # Funkcja pomocnicza wybierająca podstawową funkcję
    def choose_basic_function():
        print("\nWybierz jedną z podstawowych funkcji:")
        print(" 1. Wielomian")
        print(" 2. Trygonometryczna")
        print(" 3. Wykładnicza")
        while True:
            choice = input("Wybierz numer funkcji (1-3): ")
            if choice == "1":
                return polynomial_choose()
            elif choice == "2":
                return trigonometric_choose()
            elif choice == "3":
                return exponential_choose()
            else:
                print("Wybrano zły numer funkcji. Spróbuj ponownie.")

    # Zbieramy kolejne funkcje w liście
    functions = []
    for i in range(n):
        print(f"\nWybierz funkcję numer {i + 1} z {n}:")
        func = choose_basic_function()
        functions.append(func)

    # Definicja funkcji złożonej. Zaczyna się od najbardziej zagnieżdzonej funkcji, czyli od pierwszej podanej.
    def composite_calc(x):
        result = x
        for f in functions:
            result = f(result)
        return result

    return composite_calc


if __name__ == '__main__':
    choosed_function = choose_function()
    print(choosed_function(3.3))
