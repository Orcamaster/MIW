import random
import math

iris = []
with open("iris.txt", 'r') as plik:
    for linia in plik:
        dane = linia.rstrip().split(',')
        iris.append([float(x) if x in dane[:4] else x for x in dane])


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
    sys_test = podzial[test_index]
    sys_tren = []
    for i in range(len(podzial)):
        if i == test_index:
            continue
        for fold in podzial[i]:
            sys_tren.append(fold)

    return sys_test, sys_tren


def macierz_pomylek(predykcje, prawdziwe):
    n = len(predykcje)

    #    set ver vir
    mp = [[0, 0, 0],  # set
          [0, 0, 0],  # ver
          [0, 0, 0]]  # vir

    for x in range(n):
        if predykcje[x] == 'Iris-setosa':
            if prawdziwe[x] == 'Iris-setosa':
                mp[0][0] += 1
            elif prawdziwe[x] == 'Iris-versicolor':
                mp[0][1] += 1
            elif prawdziwe[x] == 'Iris-virginica':
                mp[0][2] += 1
        if predykcje[x] == 'Iris-versicolor':
            if prawdziwe[x] == 'Iris-setosa':
                mp[1][0] += 1
            elif prawdziwe[x] == 'Iris-versicolor':
                mp[1][1] += 1
            elif prawdziwe[x] == 'Iris-virginica':
                mp[1][2] += 1
        if predykcje[x] == 'Iris-virginica':
            if prawdziwe[x] == 'Iris-setosa':
                mp[2][0] += 1
            elif prawdziwe[x] == 'Iris-versicolor':
                mp[2][1] += 1
            elif prawdziwe[x] == 'Iris-virginica':
                mp[2][2] += 1

    print("               R. Setosa  R. Versicolor  R. Virginica")
    print(f'P.     Setosa {mp[0][0]:10} {mp[0][1]:14} {mp[0][2]:13}')
    print(f'P. Versicolor {mp[1][0]:10} {mp[1][1]:14} {mp[1][2]:13}')
    print(f'P.  Virginica {mp[2][0]:10} {mp[2][1]:14} {mp[2][2]:13}')


def srednia(zbior):
    return sum(zbior) / len(zbior)


def wariancja(zbior):
    n = len(zbior)
    sr = srednia(zbior)
    sum_x = 0

    for x in zbior:
        sum_x += (x - sr) ** 2

    return (1 / n) * sum_x


def policz_pc(sys):
    # P(A)
    prawdopodobienstwa = {}
    for klasa in sys:
        prawdopodobienstwa[klasa] = len(sys[klasa]) / len(sys)
    return prawdopodobienstwa


def policz_srednie_i_wariancje(sys):
    statystyki = {}

    for klasa, obiekt in sys.items():

        if klasa not in statystyki:
            statystyki[klasa] = []

        for i in range(4):
            wartosci = []

            for a in obiekt:
                wartosci.append(a[i])

            sr = srednia(wartosci)
            war = wariancja(wartosci)
            statystyki[klasa].append((sr, war))

    return statystyki


def policz_paic(atrybut, sr, war):
    # P(ai | C)
    ulamek = 1 / ((2 * math.pi * war) ** (1 / 2))
    potega_e = math.exp(-((atrybut - sr) ** 2) / (2 * war))
    return ulamek * potega_e


def predykuj_klasy(sys, prawdopodobienstwa, statystyki):
    predykowane_klasy = []
    prawdziwe_klasy = []

    for klasa_test in sys:

        for obiekt in sys[klasa_test]:
            wyniki = {}

            for klasa in prawdopodobienstwa:
                suma = math.log(prawdopodobienstwa[klasa])  # ln(P(C))
                stat = statystyki[klasa]

                for i in range(4):
                    sr, war = stat[i]
                    suma += math.log(policz_paic(obiekt[i], sr, war))

                wyniki[klasa] = suma

            predykcja = max(wyniki, key=wyniki.get)
            predykowane_klasy.append(predykcja)
            prawdziwe_klasy.append(klasa_test)

    return predykowane_klasy, prawdziwe_klasy


def policz_accuracy(predykcje, prawdziwe):
    n = len(predykcje)
    suma = 0

    for x in range(n):
        if predykcje[x] == prawdziwe[x]:
            suma += 1

    return (suma / n) * 100


def uruchom_algorytm(x):
    kros = kroswalidacja(iris, 5)
    wszystkie_predykcje = []
    wszystkie_prawdziwe = []

    for iteracja in range(x):
        test, tren = wybierz_systemy(kros, iteracja)
        sys_tren = {}
        sys_test = {}

        for obiekt in tren:
            klasa = obiekt[4]

            if klasa not in sys_tren:
                sys_tren[klasa] = []
            sys_tren[klasa].append(obiekt[:4])

        for obiekt in test:
            klasa = obiekt[4]

            if klasa not in sys_test:
                sys_test[klasa] = []
            sys_test[klasa].append(obiekt[:4])

        prawdopodobienstwa_klas = policz_pc(sys_tren)
        statystyki_klas = policz_srednie_i_wariancje(sys_tren)

        predykcje, prawdziwe = predykuj_klasy(sys_test, prawdopodobienstwa_klas, statystyki_klas)
        accuracy = policz_accuracy(predykcje, prawdziwe)
        print(f'{iteracja + 1}: {round(accuracy, 2)}%')

        wszystkie_predykcje.extend(predykcje)
        wszystkie_prawdziwe.extend(prawdziwe)

    total_accuracy = policz_accuracy(wszystkie_predykcje, wszystkie_prawdziwe)
    print(f'Total: {round(total_accuracy, 2)}%\n')
    macierz_pomylek(wszystkie_predykcje, wszystkie_prawdziwe)


uruchom_algorytm(5)
