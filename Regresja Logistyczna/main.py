import random
import math

australian = []
with open("australian 1.csv", 'r') as plik:
    for linia in plik:
        dane = linia.strip()
        australian.append([float(x) for x in dane.split()])


def kroswalidacja(zbior, f):
    zbior_przetasowany = zbior
    random.shuffle(zbior_przetasowany)

    podzial = []
    fold_len = len(zbior) // f

    for fold in range(f):
        podzbior = []
        for i in range(fold * fold_len, fold_len * (fold + 1)):
            podzbior.append(zbior_przetasowany[i])
        podzial.append(podzbior)
    return podzial


def wybierz_systemy(podzial, test_index):
    # test_index = indeks listy, która w danej iteracji będzie systemem testowym
    # test_index to równocześnie numer iteracji programu
    sys_test = podzial[test_index]
    sys_tren = []
    for i in range(len(podzial)):
        if i == test_index:
            continue
        for fold in podzial[i]:
            sys_tren.append(fold)

    return sys_test, sys_tren


def srednia(zbior):
    return sum(zbior) / len(zbior)


def odchylenie(zbior):
    n = len(zbior)
    sr = srednia(zbior)
    suma = 0

    for a in zbior:
        suma += (a - sr) ** 2

    return (suma / (n - 1)) ** (1 / 2)


def policz_srednie_i_odchylenia_cech(system):
    statystyki = []
    liczba_cech = len(system[0]) - 1

    for x in range(liczba_cech):
        wartosci = []

        for obiekt in system:
            wartosci.append(obiekt[x])

        srednia_cechy = srednia(wartosci)
        odchylenie_cechy = odchylenie(wartosci)
        statystyki.append((srednia_cechy, odchylenie_cechy))

    return statystyki


def przeskaluj_dane(system, statystyki):
    liczba_cech = len(system[0]) - 1
    przeskalowane_dane = []

    for obiekt in system:
        przeskalowany_obiekt = []

        for x in range(liczba_cech):
            sr, odch = statystyki[x]
            przeskalowany_obiekt.append((obiekt[x] - sr) / odch)

        przeskalowany_obiekt.append(obiekt[-1])  # klasa
        przeskalowane_dane.append(przeskalowany_obiekt)

    return przeskalowane_dane


def petla_uczenia(system, wagi, b, alfa):
    liczba_cech = len(system[0]) - 1
    liczba_obiektow = len(system)
    gradient = [0 for _ in range(liczba_cech)]
    gradient_b = 0

    for obiekt in system:
        z = b

        for x in range(liczba_cech):
            z += obiekt[x] * wagi[x]

        sigma = 1 / (1 + math.exp(- z))
        error = sigma - obiekt[-1]

        for x in range(liczba_cech):
            gradient[x] += error * obiekt[x]

        gradient_b += error

    for x in range(liczba_cech):
        gradient[x] /= liczba_obiektow
        wagi[x] -= alfa * gradient[x]

    gradient_b /= liczba_obiektow
    b -= alfa * gradient_b

    return wagi, b


def predykuj_klasy(system, wagi, b):
    liczba_cech = len(system[0]) - 1
    predykowane_klasy = []

    for obiekt in system:
        z = b

        for x in range(liczba_cech):
            z += obiekt[x] * wagi[x]

        sigma = 1 / (1 + math.exp(- z))

        if sigma >= 0.5:
            predykowane_klasy.append(1)
        else:
            predykowane_klasy.append(0)

    return predykowane_klasy


def policz_accuracy(system, predykcje):
    liczba_obiektow = len(system)
    suma = 0

    for x in range(liczba_obiektow):
        if system[x][-1] == predykcje[x]:
            suma += 1

    return (suma / liczba_obiektow) * 100


def uruchom(x):
    kros = kroswalidacja(australian, x)
    total_accuracy = 0

    for iteracja in range(x):
        test, trening = wybierz_systemy(kros, iteracja)

        srednie_i_odchylenia = policz_srednie_i_odchylenia_cech(trening)
        przeskalowany_trening = przeskaluj_dane(trening, srednie_i_odchylenia)
        przeskalowany_test = przeskaluj_dane(test, srednie_i_odchylenia)

        wektor_wag = [0 for _ in range(len(trening[0]))]
        bias = 0
        learning_rate = 0.01
        liczba_iteracji = 100

        for i in range(liczba_iteracji):
            petla_uczenia(przeskalowany_trening, wektor_wag, bias, learning_rate)

        predykcje = predykuj_klasy(test, wektor_wag, bias)
        accuracy = policz_accuracy(przeskalowany_test, predykcje)
        total_accuracy += accuracy
        print(f'{iteracja + 1}: {round(accuracy, 2)}%')

    total_accuracy /= x
    print(f'Total: {round(total_accuracy, 2)}%')


uruchom(6)
