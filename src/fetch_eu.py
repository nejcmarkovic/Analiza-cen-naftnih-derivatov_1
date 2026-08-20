
import pandas as pd
import requests

URL = (
    "https://energy.ec.europa.eu/document/download/"
    "906e60ca-8b6a-44e7-8589-652854d2fd3f_en"
    "?filename=Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx"
)

XLSX_PATH = "data/raw/eu_zgodovina.xlsx"
CSV_PATH = "data/raw/eu_cene.csv"

DRZAVE = {
    "SI": "Slovenija",
    "AT": "Avstrija",
    "IT": "Italija",
}


def prenesi_datoteko(url=URL, pot=XLSX_PATH):


    
    odziv = requests.get(url, timeout=30)
    odziv.raise_for_status()
    with open(pot, "wb") as f:
        f.write(odziv.content)
    print("Datoteka prenesena v", pot)


def izlusci_cene(pot=XLSX_PATH):
    tabela = pd.read_excel(pot, sheet_name="Prices with taxes")

    
    ime_datumskega_stolpca = tabela.columns[0]
    tabela = tabela.rename(columns={ime_datumskega_stolpca: "datum"})

    
    tabela = tabela.iloc[2:].reset_index(drop=True)

    nova_tabela = pd.DataFrame()
    nova_tabela["datum"] = pd.to_datetime(tabela["datum"], errors="coerce")

    for koda, ime in DRZAVE.items():
        stolpec_bencin = koda + "_price_with_tax_euro95"
        stolpec_dizel = koda + "_price_with_tax_diesel"
        nova_tabela[ime + "_bencin"] = pd.to_numeric(tabela[stolpec_bencin], errors="coerce")
        nova_tabela[ime + "_dizel"] = pd.to_numeric(tabela[stolpec_dizel], errors="coerce")

    nova_tabela = nova_tabela.dropna(subset=["datum"])
    nova_tabela = nova_tabela.sort_values("datum").reset_index(drop=True)
    return nova_tabela


def shrani(tabela, pot=CSV_PATH):
    tabela.to_csv(pot, index=False)
    print(f"Shranjenih {len(tabela)} vrstic v {pot}")


if __name__ == "__main__":
    prenesi_datoteko()
    cene = izlusci_cene()
    shrani(cene)
