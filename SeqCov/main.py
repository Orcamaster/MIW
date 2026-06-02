from itertools import combinations

sys = []
with open("plik.txt", "r") as plik:
    for linia in plik:
        ob = {}
        dane = [int(x) for x in linia.strip().split()]
        for x in range(len(dane) - 1):
            ob[f'A{x + 1}'] = dane[x]
        ob['D'] = dane[-1]
        sys.append(ob)


def sequential_covering(system):
    liczba_atrybutow = len(system[0]) - 1
    niepokryte_obiekty = system.copy()
    reguly = {}

    atrybuty = []
    for i in range(liczba_atrybutow):
        atrybuty.append(f"A{i + 1}")

    rzad = 1

    while len(niepokryte_obiekty) > 0:
        czy_reguly_w_rzedzie = False

        for kombinacja in combinations(atrybuty, rzad):

            for obiekt in niepokryte_obiekty:
                decyzja_obiektu = obiekt["D"]

                wartosci = {}
                for atrybut in kombinacja:
                    wartosci[atrybut] = obiekt[atrybut]

                pasujace_obiekty = []
                for inny_obiekt in system:
                    pasuje = True

                    for atrybut in kombinacja:
                        if inny_obiekt[atrybut] != wartosci[atrybut]:
                            pasuje = False
                            break

                    if pasuje is True:
                        pasujace_obiekty.append(inny_obiekt)

                decyzje = set()
                for o in pasujace_obiekty:
                    decyzje.add(o["D"])

                if len(decyzje) == 1:
                    support = 0
                    for o in pasujace_obiekty:
                        if o["D"] == decyzja_obiektu:
                            support += 1

                    tekst = wypisz_regule(kombinacja, wartosci, decyzja_obiektu)
                    reguly[tekst] = support
                    czy_reguly_w_rzedzie = True

                    pokryte_obiekty = []
                    for ob in niepokryte_obiekty:
                        pasuje = True

                        for atrybut in kombinacja:
                            if ob[atrybut] != wartosci[atrybut]:
                                pasuje = False
                                break

                        if pasuje is True:
                            pokryte_obiekty.append(ob)

                    for ob in pokryte_obiekty:
                        niepokryte_obiekty.remove(ob)

        if not czy_reguly_w_rzedzie:
            rzad += 1
            if rzad > liczba_atrybutow:
                break

    return reguly


def wypisz_regule(comb, wart, dec):
    tekst = "("

    for i in range(len(comb)):
        nazwa = comb[i]
        tekst += f'{nazwa} = {wart[nazwa]}'

        if i < len(comb) - 1:
            tekst += " ^ "

    tekst += f') => (D = {dec})'

    return tekst


powstale_reguly = sequential_covering(sys)
for p in powstale_reguly:
    print(f'{p} [{powstale_reguly[p]}]')
