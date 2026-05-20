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


def skalowanie(x, sr, odch):
    return (x - sr) / odch


def petla_uczenia(probka, wagi, b, alfa):
    z = b
    for i in range(14):
        z += probka[i] * wagi[i]

    y_prim = 1 / (1 + math.exp(- z))


wektor_wag = [0 for x in range(14)]
bias = 0
a = 0.01

kros = kroswalidacja(australian, 6)
test, tren = wybierz_systemy(kros, 3)
