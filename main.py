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

        """ewentualnie mozna dac zamiast exception ValueError"""
        raise Exception("Błąd! Funkcja nie ma różnych znaków na krańcach przedziału!")
    else:
        # W pętli wyznaczamy kolejne przybliżenia pierwiastk
        count = 0
        prev_x = None
        while True:
            x0 = (fa * b - fb * a) / (fa - fb)

            # Warunki stopu
            if isIterations:
                iterations -= 1
                count += 1
                if iterations <= 0:
                    return x0, count
            else:
                # Warunek stopu wariant A
                if prev_x is not None and abs(x0 - prev_x) < accuracy:
                    return x0, 0
            prev_x = x0

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
    isIterations = True if iterations > 0 else False

    # obliczamy i zapamietujemy wartosci funkcji na keancach przedzialu
    fa = function(a)
    fb = function(b)

    if fa * fb >= 0:
        raise Exception("Błąd! Funkcja nie ma różnych znaków na krańcach przedziału!")
    count = 0
    prev_x = None
    while True:
        x0 = (a + b) / 2.0 #srodek przedzialu
        fx = function(x0)

        #warunki stopu
        if isIterations:
            iterations -= 1
            count += 1
            if iterations <= 0:
                return x0, count
        else:
            if prev_x is not None and abs(x0 - prev_x) < accuracy:
                return x0, 0
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


def plot_function(func, x0, a=-2, b=2, points=1000):
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

    plt.plot(x0, func(x0), 'ro', markersize=8, label="Przybliżone miejsce zerowe")

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
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
        print(" 2. Dokładność (np. 1e-5)")
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
                user_input = input("Podaj dokładność (np. 1e-5): ")
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

    method = None
    while method not in ["1","2"]:
        print("\nWybierz metodę numeryczną:")
        print(" 1. Regula falsi")
        print(" 2. Metoda bisekcji")
        method = input("Wprowadź 1 lub 2: ")


    if mode == "iter":
        iterations = value
        accuracy = 1e-10 # tu dalismy domyslna mala dokladnosc, gdy liczymy na iteracje
    else:
        iterations = 0
        accuracy = value

    if method == "1":
        x0, total_iterations = falsi(range_start, range_end, accuracy, iterations, function)
    else:
        x0, total_iterations = bisection(range_start, range_end, accuracy, iterations, function)


    plot_function(function, x0, range_start, range_end)

    print("\n===== ROZWIĄZANIE =====")
    print(f"Obliczone miejsce zerowe {x0}.")
    if total_iterations != 0:
        print(f"Liczba wykonanych iteracji: {total_iterations}.")
    else:
        print("\nUżyto dokładności: " + str(accuracy))
