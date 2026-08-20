
import pandas as pd


def povprecne_cene(tabela, stolpci):
    """Vrne povprecno ceno za vsak podan stolpec, urejeno od najnizje do najvisje."""
    return tabela[stolpci].mean().sort_values()


def razlika_do_referencne(tabela, stolpci, referencni_stolpec):
    """
    Za vsak stolpec iz seznama izracuna razliko do referencnega stolpca
    (npr. za vsako drzavo, koliko je drazja/cenejsa od Slovenije).
    Vrne nov DataFrame z datumom in stolpci razlik.
    """
    razlike = pd.DataFrame()
    razlike["datum"] = tabela["datum"]

    for stolpec in stolpci:
        if stolpec == referencni_stolpec:
            continue
        ime_novega_stolpca = stolpec + "_razlika"
        razlike[ime_novega_stolpca] = tabela[stolpec] - tabela[referencni_stolpec]

    return razlike


def korelacijska_matrika(tabela, stolpci):
    """Vrne korelacijsko matriko med podanimi stolpci (drzavami)."""
    return tabela[stolpci].corr()


def najvecja_razlika(tabela, stolpec_a, stolpec_b):
    """
    Poisce datum, ko je bila razlika med dvema stolpcema (drzavama)
    najvecja, in vrne ta datum ter velikost razlike.
    """
    razlike = (tabela[stolpec_a] - tabela[stolpec_b]).abs()
    indeks_najvecje = razlike.idxmax()
    return tabela.loc[indeks_najvecje, "datum"], razlike[indeks_najvecje]
