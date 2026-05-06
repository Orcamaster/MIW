import math
file = open("iris.txt", 'r')

sys_tren = {}
sys_test = {}
prawd_klas = {}
stat_klas = {}

# Separacja danych
i = 1
for linia in file.readlines():
    dane = linia.rstrip().split(',')
    if i <= 30:
        if dane[4] not in sys_test:
            sys_test[dane[4]] = []
        sys_test[dane[4]].append(dane[:4])
    else:
        if dane[4] not in sys_tren:
            sys_tren[dane[4]] = []
        sys_tren[dane[4]].append(dane[:4])
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


# Obliczanie P(A) dla każdej klasy
def p_c(sys):
    for klasa in sys:
        prawd_klas[klasa] = round(len(sys[klasa]) / 120, 3)


# Obliczanie średniej i wariancji dla każdego atrybutu
def srednie_i_wariancje(sys):
    for klasa, obiekt in sys.items():
        print(klasa)
        for i in range(4):
            wartosci = [float(x[i]) for x in obiekt]  # Lista wartości dla obecnego atrybutu.
            sr = round(srednia(wartosci), 3)
            war = round(wariancja(wartosci), 3)

            if klasa not in stat_klas:
                stat_klas[klasa] = []
            stat_klas[klasa].append((sr, war))


# Obliczanie P(ai | C)
def p_aic(atrybut, sr, war):
    ulamek = 1 / ((2 * math.pi * (war ** 2)) ** (1 / 2))
    potega_e = math.exp(-(atrybut - sr) ** 2) / (2 * (war ** 2))
    return ulamek * potega_e


def suma_log(prawdopodobienstwa, statystyki):
    for klasa, wartosc in prawdopodobienstwa.items():
        log_pc = math.log(prawdopodobienstwa[klasa])


    return


srednie_i_wariancje(sys_tren)
print(stat_klas)

p_c(sys_tren)
print(prawd_klas)
