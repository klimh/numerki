from math import sin
import matplotlib.pyplot as plt
import numpy as np

from functions import choose_function


def falsi(a: float, b: float, accuracy: float, iterations: int, function):
    """Funkcja obliczają bliżone miejsce zerowe regula falsi.
    Przyjmuje:
    :parameter a : float - początek przedziału
    :parameter b : float - koniec przedziału
    :parameter accuracy : float - przybliżenie szacowania
    :parameter iterations : int - liczbę iteracji algorytmu do wykonania. Jeśli iterations <=0, to warunkiem stopu będzie dokładnością.
    W przeciwnym przypadku warunkiem stopu jest podana liczba iteracji.

    :returns przybliżone miejsce zerowe : float
    :returns liczba wykonanych iteracji (zwraca 0 jeśli wybraną warunek stopu z  dokładnością): int
    """
    # Warunek stopu
    isIterations = True
    if iterations <= 0:
        isIterations = False

    # Obliczamy i zapamiętujemy wartości funkcji na krańcach przedziału [a,b]
    fa = function(a)
    fb = function(b)

    """tu mozna ulatwic i odrazu dac function(a) * function(b) > 0"""
    if fa * fb > 0:

        raise ValueError("Błąd! Funkcja nie ma różnych znaków na krańcach przedziału!")
    else:
        # W pętli wyznaczamy kolejne przybliżenia pierwiastk
        count = 0
        prev_x = None
        while True:
            x0 = (fa * b - fb * a) / (fa - fb)

            # Warunki stopu
            if isIterations:
                iterations -= 1
                if iterations <= 0:
                    return x0, count
            else:
                # Warunek stopu wariant A
                if prev_x is not None and abs(x0 - prev_x) < accuracy:
                    return x0, count
            prev_x = x0
            count += 1

            fx = function(x0)

            # Za nowy przedział [a,b] przyjmujemy tą z części [a,x0], [x0,b],
            # w której funkcja ma różne znaki na krańcach
            if fa * fx < 0:
                b = x0
                fb = fx
            else:
                a = x0
                fa = fx

def bisection(a: float, b: float, accuracy: float, iterations: int, function):
    """Funkcja oblicza przybliżone miejsce zerowe metodą bisekcji.
    Przyjmuje:
    :parameter a : float - początek przedziału
    :parameter b : float - koniec przedziału
    :parameter accuracy : float - przybliżenie szacowania
    :parameter iterations : int - liczba iteracji algorytmu do wykonania. Jeśli iterations <=0, to warunkiem stopu będzie dokładność.
    W przeciwnym przypadku warunkiem stopu jest podana liczba iteracji.

    :returns przybliżone miejsce zerowe : float
    :returns liczba wykonanych iteracji (zwraca 0 jeśli wybrano warunek stopu z dokładnością): int
    """
    # warunek stopu
    isIterations = iterations > 0

    # obliczamy i zapamietujemy wartosci funkcji na krańcach przedzialu
    fa = function(a)
    fb = function(b)

    if fa * fb >= 0:
        raise ValueError("Błąd! Funkcja nie ma różnych znaków na krańcach przedziału!")
    count = 0
    prev_x = None
    while True:
        x0 = (a + b) / 2.0 #srodek przedzialu
        fx = function(x0)
        count += 1

        if fx == 0:
            return  x0, count

        #warunki stopu
        if isIterations:
            if fx == 0:
                return x0, count

            iterations -= 1
            count += 1

            if iterations <= 0:
                return x0, count
        else:
            if fx == 0:
                return x0, count

            if prev_x is not None and abs(x0 - prev_x) < accuracy:
                return x0, count
        prev_x = x0

        #wybieramy nowy przedzial
        if fa * fx < 0:
            b = x0
            fb = fx
        else:
            a = x0
            fa = fx

def choose_range():
    start = None
    while start is None:
        try:
            start = float(input("Podaj początek badanego przedziału: "))
        except ValueError:
            print("Błąd: niepoprawna wartość.")

    end = None
    while end is None or end <= start:
        try:
            end = float(input("Podaj koniec badanego przedziału: "))
            if end <= start:
                print("Błąd: koniec przedziału nie może być mniejszy lub równy początkowi przedziału.")
        except ValueError:
            print("Błąd: niepoprawna wartość.")
    return start, end


def plot_function(func, x0_falsi, x0_bisection, a=-2, b=2, points=1000):
    """
    Rysuje wykres funkcji w zadanym przedziale [a, b].

    :param func: Funkcja do narysowania (powinna przyjmować jeden argument x).
    :param a: Początek przedziału (domyślnie -2).
    :param b: Koniec przedziału (domyślnie 2).
    :param points: Liczba punktów na wykresie (domyślnie 1000).
    """
    x_values = np.linspace(a, b, points)
    y_values = np.array([func(x) for x in x_values])

    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, label="f(x)", color='b')
    plt.axhline(0, color='black', linewidth=0.8)  # Oś OX
    plt.axvline(0, color='black', linewidth=0.8)  # Oś OY

    plt.plot(x0_falsi, func(x0_falsi), 'go', markersize=10, label="Przybliżone miejsce zerowe dla reguly falsi")
    plt.plot(x0_bisection, func(x0_bisection), 'mo', markersize=8, label="Przybliżone miejsce zerowe dla metody bisekcji")

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show()


def choose_stop_condition():
    """
    Pozwala użytkownikowi wybrać warunek stopu:
      - "1": liczba iteracji (wartość całkowita > 0)
      - "2": dokładność (wartość dodatnia, np. 1e-5)

    Zwraca krotkę:
      - ('iter', liczba_iteracji) lub ('accuracy', dokładność)
    """
    stop_mode = None
    # Pętla wyboru trybu stopu
    while stop_mode is None:
        print("Wybierz warunek stopu:")
        print(" 1. Liczba iteracji")
        print(" 2. Dokładność ε (np. 1e-5)")
        mode_input = input("Wprowadź 1 lub 2: ")
        if mode_input == "1":
            stop_mode = "iter"
        elif mode_input == "2":
            stop_mode = "accuracy"
        else:
            print("Błąd: wybierz 1 lub 2.")

    # Jeśli użytkownik wybrał warunek oparty na liczbie iteracji:
    if stop_mode == "iter":
        num_iterations = None
        while num_iterations is None or num_iterations <= 0:
            try:
                user_input = input("Podaj liczbę iteracji (liczba całkowita > 0): ")
                num_iterations_temp = int(user_input)
                if num_iterations_temp <= 0:
                    print("Błąd: liczba iteracji musi być większa od 0.")
                else:
                    num_iterations = num_iterations_temp
            except ValueError:
                print("Błąd: podaj poprawną liczbę całkowitą.")
        return "iter", num_iterations
    else:
        # Jeśli użytkownik wybrał warunek oparty na dokładności:
        accuracy = None
        while accuracy is None or accuracy <= 0:
            try:
                user_input = input("Podaj dokładność ε(np. 1e-5): ")
                accuracy_temp = float(user_input)
                if accuracy_temp <= 0:
                    print("Błąd: dokładność musi być większa od 0.")
                else:
                    accuracy = accuracy_temp
            except ValueError:
                print("Błąd: podaj poprawną wartość liczbową (np. 1e-5).")
        return "accuracy", accuracy

if __name__ == '__main__':
    range_start, range_end = choose_range()
    function = choose_function()
    mode, value = choose_stop_condition()

    if mode == "iter":
        iterations = value
        accuracy = 0
    else:
        iterations = 0
        accuracy = value

    try:
        x0_falsi, iterations_falsi = falsi(range_start, range_end, accuracy, iterations, function)
        x0_bisection, iterations_bisection = bisection(range_start, range_end, accuracy, iterations, function)
    except ValueError:
        print("Błąd! Funkcja nie ma różnych znaków na krańcach przedziału!")
        exit()


    plot_function(function, x0_falsi, x0_bisection, range_start, range_end)


    print("\n===== ROZWIĄZANIE =====")
    if iterations == 0:
        #Warunek stopu: dokładność
        print(f"Obliczone miejsca zerowe:\nMetodą bisekcji: {x0_bisection} Liczba wykonanych iteracji: {iterations_bisection}\nMetodą falsi: {x0_falsi} Liczba wykonanych iteracji: {iterations_falsi}.")
    else:
        #Warunek stopu: liczba iteracji
        print(f"Obliczone miejsca zerowe:\nMetodą bisekcji: {x0_bisection}\nMetodą falsi: {x0_falsi}.")
