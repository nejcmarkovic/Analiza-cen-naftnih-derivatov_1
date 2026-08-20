import pandas as pd


def drsece_povprecje(tabela, stolpec, okno=30):
    tabela = tabela.copy()
    ime_stolpca = stolpec + "_drsece_" + str(okno) + "d"
    tabela[ime_stolpca] = tabela[stolpec].rolling(window=okno).mean()
    return tabela

def korelacija(tabela, stolpec_1, stolpec_2):
    return tabela[stolpec_1].corr(tabela[stolpec_2])

def volatilnost(tabela, stolpec, okno=30):
    donosi = tabela[stolpec].pct_change()
    return donosi.rolling(window=okno).std() * 100

if __name__=="__main__":
    cene = pd.read_csv("data/processed/cene.csv", parse_dates=["datum"])

    korelacija1 = korelacija(cene, "bencin_95", "brent")
    print("Korelacija med ceno bencina in Brent nafto:", round(korelacija, 3))

    cene = drsece_povprecje(cene, "bencin_95", okno=30)
    print(cene.tail())