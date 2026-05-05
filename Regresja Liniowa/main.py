import matplotlib.pyplot as plt  # 3.10.9
import numpy as np

plik = open("dane.txt", "r")
zbior_x = []
zbior_y = []

for linia in plik:
    dane = linia.split()
    zbior_x.append(int(dane[0]))
    zbior_y.append(int(dane[1]))


def srednia(zbior):
    return sum(zbior) / len(zbior)


def odchylenie(zbior):
    n = len(zbior)
    M = srednia(zbior)
    suma = 0

    for a in zbior:
        suma += (a - M) ** 2

    return (suma / (n - 1)) ** (1 / 2)


def korelacja(zb_x, zb_y):
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    sum_x = sum(zb_x)
    sum_y = sum(zb_y)
    n = len(zb_x)

    for i in range(0, n):
        sum_x2 += zb_x[i] ** 2
        sum_y2 += zb_y[i] ** 2
        sum_xy += zb_x[i] * zb_y[i]

    licznik = (n * sum_xy - sum_x * sum_y)
    mianownik = (((n * sum_x2) - (sum_x ** 2)) * ((n * sum_y2) - (sum_y ** 2))) ** (1 / 2)
    return licznik / mianownik


def funkcja_liniowa(zb_x, zb_y, x):
    wsp_b = korelacja(zb_x, zb_y) * (odchylenie(zb_y) / odchylenie(zb_x))
    wsp_a = srednia(zb_y) - (wsp_b * srednia(zb_x))
    return wsp_b * x + wsp_a


print(funkcja_liniowa(zbior_x, zbior_y, 6.0))
x_linia = np.linspace(0, max(zbior_x), 100)
y_linia = funkcja_liniowa(zbior_x, zbior_y, x_linia)

plt.figure()
plt.scatter(zbior_x, zbior_y, label="Wartości niezależne")
plt.plot(x_linia, y_linia, color='red', label="Linia regresji")
plt.xlabel("Wartości X")
plt.ylabel("Wartości Y")
plt.legend()
plt.show()
