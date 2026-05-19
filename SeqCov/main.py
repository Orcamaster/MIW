from itertools import combinations

sys = []
with open("plik.txt", "r") as plik:
    index = 1
    for linia in plik:
        ob = {'ob': f'{id}'}
        dane = [int(x) for x in linia.strip().split()]
        for x in range(len(dane) - 1):
            ob[f'A{x + 1}'] = dane[x]
        ob['D'] = dane[-1]
        sys.append(ob)
        index += 1


def sequential_covering(system):
    reguly = {}
    niepokryte = system.copy()
    ilosc_atrybutow = len(system[0]) - 2

    atrybuty = []
    for i in range(ilosc_atrybutow):
        atrybuty.append(f"A{i + 1}")

    rzad = 1

    while len(niepokryte) > 0:
        czy_reguly_w_rzedzie = False

        for kombinacja in combinations(atrybuty, rzad):
            for obiekt in niepokryte:
                decyzja_obiektu = obiekt["D"]
                wartosci = {}

                for atrybut in kombinacja:
                    wartosci[atrybut] = obiekt[atrybut]

                dopasowane = []
                for inny_obiekt in system:
                    pasuje = True
                    for atrybut in kombinacja:
                        if inny_obiekt[atrybut] != wartosci[atrybut]:
                            pasuje = False
                            break
                    if pasuje:
                        dopasowane.append(inny_obiekt)

                decyzje = set()
                for o in dopasowane:
                    decyzje.add(o["D"])

                if len(decyzje) == 1:
                    support = 0
                    for o in dopasowane:
                        if o["D"] == decyzja_obiektu:
                            support += 1

                    tekst = tekst_reguly(kombinacja, wartosci, decyzja_obiektu)
                    reguly[tekst] = support
                    czy_reguly_w_rzedzie = True

                    pokryte = []
                    for ob in niepokryte:
                        pasuje = True
                        for atrybut in kombinacja:
                            if ob[atrybut] != wartosci[atrybut]:
                                pasuje = False
                                break
                        if pasuje:
                            pokryte.append(ob)

                    for ob in pokryte:
                        niepokryte.remove(ob)

        if not czy_reguly_w_rzedzie:
            rzad += 1
            if rzad > ilosc_atrybutow:
                break

    return reguly


def tekst_reguly(comb, wart, dec):
    tekst = "("
    for i in range(len(comb)):
        nazwa = comb[i]
        tekst += f"{nazwa} = {wart[nazwa]}"
        if i < len(comb) - 1:
            tekst += " ^ "
    tekst += f") => (D = {dec})"
    return tekst


powstale_reguly = sequential_covering(sys)
for p in powstale_reguly:
    print(f'{p} [{powstale_reguly[p]}]')
