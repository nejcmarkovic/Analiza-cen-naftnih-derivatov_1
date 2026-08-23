
import pandas as pd


def povprecne_cene(tabela, stolpci):
    
    return tabela[stolpci].mean().sort_values()


def razlika_do_referencne(tabela, stolpci, referencni_stolpec):



   
    razlike = pd.DataFrame()
    razlike["datum"] = tabela["datum"]

    for stolpec in stolpci:
        if stolpec == referencni_stolpec:
            continue
        ime_novega_stolpca = stolpec + "_razlika"
        razlike[ime_novega_stolpca] = tabela[stolpec] - tabela[referencni_stolpec]

    return razlike


def korelacijska_matrika(tabela, stolpci):
    
    return tabela[stolpci].corr()


def najvecja_razlika(tabela, stolpec_a, stolpec_b):


    
    razlike = (tabela[stolpec_a] - tabela[stolpec_b]).abs()
    indeks_najvecje = razlike.idxmax()
    return tabela.loc[indeks_najvecje, "datum"], razlike[indeks_najvecje]
