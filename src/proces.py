import pandas as pd

slo_cene = "data/raw/si_cene_derivatov.csv"
svet_cene = "data/raw/svetovne_cene_nafte.csv"
output = "data/processed/cene.csv"


def preberi_podatke(si_pot=slo_cene, svet_pot=svet_cene):
    si_cene = pd.read_csv(si_pot, parse_dates=["datum"])
    svetovne_cene = pd.read_csv(svet_pot, parse_dates=["datum"])
    return si_cene, svetovne_cene

def dnevni_nivo(tabela):
    tabela = tabela.set_index("datum").asfreq("D").ffill()
    return tabela.reset_index()

def zdruzi_podatke(si_cene, svetovne_cene):
    si_cene_dnevno = dnevni_nivo(si_cene)
    zdruzeno = pd.merge(si_cene_dnevno, svetovne_cene, on="datum", how="inner")
    return zdruzeno

def shrani(tabela, pot=output):
    tabela.to_csv(pot, index=False)
    print(f"Shranjenih {len(tabela)} vrstic v {pot}")

if __name__ == "__main__":
    si_cene, svetovne_cene = preberi_podatke()
    zdruzeno = zdruzi_podatke(si_cene, svetovne_cene)
    shrani(zdruzeno)
    