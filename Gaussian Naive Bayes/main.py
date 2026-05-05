import math
import numpy as np
np.set_printoptions(legacy='1.25')
file = open("iris.txt", 'r')

sys_tren = {}
sys_test = {}
prawd_klas = {}
stat_klas = {}

# Separacja danych
i = 1
for linia in file.readlines():
    dane = linia.rstrip().split(',')
    if i <= 120:
        if dane[4] not in sys_tren:
            sys_tren[dane[4]] = []
        sys_tren[dane[4]].append(dane[:4])
    else:
        if dane[4] not in sys_test:
            sys_test[dane[4]] = []
        sys_test[dane[4]].append(dane[:4])
    i += 1


# Obliczanie P(A) dla każdej klasy
for klasa in sys_tren:
    prawd_klas[klasa] = len(sys_tren[klasa]) / 120


# Obliczanie średniej i wariancji dla każdego atrybutu
for klasa, obiekt in sys_tren.items():
    print(klasa)
    for i in range(4):
        wartosci = [float(x[i]) for x in obiekt]    # Lista wartości dla obecnego atrybutu.
        srednia = np.average(wartosci)
        wariancja = np.var(wartosci)

        if klasa not in stat_klas:
            stat_klas[klasa] = []
        stat_klas[klasa].append((srednia, wariancja))

print(prawd_klas)
print(stat_klas)


def p_aic(atrybut, sr, war):
    ulamek = 1 / (math.sqrt(2 * math.pi * (war ** 2)))
    potega_e = math.exp(-(atrybut - sr) ** 2) / (2 * (war ** 2))
    return ulamek * potega_e


# TODO: Krok 3
