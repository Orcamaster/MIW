import math
import random

iris_dane = []
with open("iris.txt", 'r') as plik:
    for linia in plik:
        dane = linia.rstrip().split(',')
        iris_dane.append([float(x) if x in dane[:4] else x for x in dane])


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


def srednia(zbior):
    return sum(zbior) / len(zbior)


def wariancja(zbior):
    n = len(zbior)
    sr = srednia(zbior)
    sum_x = 0

    for x in zbior:
        sum_x += (x - sr) ** 2
    return (1 / n) * sum_x


def p_c(sys):
    """Obliczanie P(A) dla każdej klasy"""
    prawdopodobienstwa = {}
    for klasa in sys:
        prawdopodobienstwa[klasa] = len(sys[klasa]) / len(sys)
    return prawdopodobienstwa


def srednie_i_wariancje(sys):
    """Obliczanie średniej i wariancji dla każdego atrybutu"""
    statystyki = {}
    for klasa, obiekt in sys.items():
        for i in range(4):
            wartosci = [x[i] for x in obiekt]  # Lista wartości dla obecnego atrybutu
            sr = srednia(wartosci)
            war = wariancja(wartosci)

            if klasa not in statystyki:
                statystyki[klasa] = []
            statystyki[klasa].append((sr, war))
    return statystyki


def p_aic(atrybut, sr, war):
    """Obliczanie P(ai | C)"""
    ulamek = 1 / ((2 * math.pi * (war ** 2)) ** (1 / 2))
    potega_e = math.exp(-(atrybut - sr) ** 2) / (2 * (war ** 2))
    return ulamek * potega_e


def sumy_logarytmow(sys, prawdopodobienstwa, statystyki):
    """Obliczanie sum i predykowanie klas"""
    predykcje = []
    for klasa_test in sys:  # Przejście przez klucze (klasy) do rozpakowania obiektów
        for obiekt in sys[klasa_test]:  # Przejście przez wartości kluczy (obiekty)
            wyniki = {}  # Klasy i ich sumy

            for klasa in prawdopodobienstwa:
                suma = math.log(prawdopodobienstwa[klasa])  # ln(P(C))
                stat = statystyki[klasa]  # Wczytanie statystyk aktualnej klasy

                for i in range(4):
                    sr, war = stat[i]
                    suma += math.log(p_aic(obiekt[i], sr, war))
                wyniki[klasa] = suma

            predykcja = max(wyniki, key=wyniki.get)

            if predykcja == klasa_test:
                # print(f'C: {klasa_test}, P: \033[32m{predykcja}\033[0m')
                predykcje.append(1)  # Poprawna
            else:
                # print(f'C: {klasa_test}, P: \033[31m{predykcja}\033[0m')
                predykcje.append(0)  # Niepoprawna

    accuracy = sum(predykcje) / len(predykcje)
    return accuracy


def uruchom_algorytm(x):
    accuracies = []
    foldy = kroswalidacja(iris_dane, 5)

    for i in range(x):
        sys_tren = {}
        sys_test = {}

        for fold in foldy:
            for obiekt in fold:
                if foldy.index(fold) == i:
                    if obiekt[4] not in sys_test:
                        sys_test[obiekt[4]] = []
                    sys_test[obiekt[4]].append([x for x in obiekt[:4]])
                else:
                    if obiekt[4] not in sys_tren:
                        sys_tren[obiekt[4]] = []
                    sys_tren[obiekt[4]].append([x for x in obiekt[:4]])

        prawdopodobienstwa_klas = p_c(sys_tren)
        statystyki_klas = srednie_i_wariancje(sys_tren)
        accuracies.append(sumy_logarytmow(sys_test, prawdopodobienstwa_klas, statystyki_klas))

    final_accuracy = sum(accuracies) / len(accuracies)
    print(accuracies)
    print(final_accuracy)


uruchom_algorytm(5)
