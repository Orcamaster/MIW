import math

file = open("iris.txt", 'r')

sys_tren = {}
sys_test = {}
prawd_klas = {}
stat_klas = {}

i = 1
for linia in file.readlines():
    dane = linia.rstrip().split(',')
    if i <= 30:
        if dane[4] not in sys_test:
            sys_test[dane[4]] = []
        sys_test[dane[4]].append([float(x) for x in dane[:4]])
    else:
        if dane[4] not in sys_tren:
            sys_tren[dane[4]] = []
        sys_tren[dane[4]].append([float(x) for x in dane[:4]])
    i += 1


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
    for klasa in sys:
        prawd_klas[klasa] = round(len(sys[klasa]) / 120, 3)


def srednie_i_wariancje(sys):
    """Obliczanie średniej i wariancji dla każdego atrybutu"""
    for klasa, obiekt in sys.items():
        for i in range(4):
            wartosci = [float(x[i]) for x in obiekt]  # Lista wartości dla obecnego atrybutu
            sr = round(srednia(wartosci), 3)
            war = round(wariancja(wartosci), 3)

            if klasa not in stat_klas:
                stat_klas[klasa] = []
            stat_klas[klasa].append((sr, war))


def p_aic(atrybut, sr, war):
    """Obliczanie P(ai | C)"""
    ulamek = 1 / ((2 * math.pi * (war ** 2)) ** (1 / 2))
    potega_e = math.exp(-(atrybut - sr) ** 2) / (2 * (war ** 2))
    return ulamek * potega_e


def sumy_logarytmow(prawdopodobienstwa, statystyki):
    predykcje = []
    for klasa_test in sys_test:  # Przejście przez klucze (klasy)
        for obiekt in sys_test[klasa_test]:  # Przejście przez wartości kluczy (obiekty)
            wynik = {}  # Sumy

            for klasa in prawdopodobienstwa:
                suma = math.log(prawdopodobienstwa[klasa])  # ln(P(C))
                stat = statystyki[klasa]  # Wczytanie statystyk aktualnej klasy

                for i in range(4):
                    srednia = stat[i][0]
                    wariancja = stat[i][1]

                    suma += math.log(p_aic(obiekt[i], srednia, wariancja))

                wynik[klasa] = suma

            predykcje.append(max(wynik, key=wynik.get))

    return predykcje


srednie_i_wariancje(sys_tren)
# print(stat_klas)

p_c(sys_tren)
# print(prawd_klas)

sumy_logarytmow(prawd_klas, stat_klas)

# TODO: accuracy = poprawne predykcje / liczba próbek zbioru testowego
# TODO: kroswalidacja (5 foldów)
