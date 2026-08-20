from datetime import datetime, timezone

import pandas as pd
import requests

Tickerji = {"BZ=F": "brent", "CL=F": "wti"}
output = "data/raw/svetovne_cene_nafte.csv"

def sistemski_cas(datum_niz):
    dt =datetime.strptime(datum_niz, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp())
def prenesi_ticker(ticker, zacetek, konec):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/" + ticker

    if konec:
        konec_cas = sistemski_cas(konec)
    else:
        konec_cas =int(datetime.now(timezone.utc).timestamp())

    parametri = {
        "period1": sistemski_cas(zacetek),
        "period2": konec_cas,
        "interval": "1d",
    }
    glave = {"User-Agent": "Mozilla/5.0"}

    odziv = requests.get(url, params=parametri, headers=glave, timeout=10)
    odziv.raise_for_status()
    podatki = odziv.json()

    rezultat = podatki["chart"]["result"][0]
    casovni_zigi = rezultat["timestamp"]
    zapiralne_cene = rezultat["indicators"]["quote"][0]["close"]

    cene_po_datumih = {}

    for zig, cena in zip(casovni_zigi, zapiralne_cene):
        if cena is None:
            continue
        datum = datetime.fromtimestamp(zig, tz=timezone.utc).strftime("%Y-%m-%d")
        cene_po_datumih[datum] = round(cena, 3)
    return cene_po_datumih

def zajemi_cene_nafte(zacetek="2020-01-01", konec=None):
    cene_izdelki = {}
    for ticker, ime in Tickerji.items():
        cene_izdelki[ime] = prenesi_ticker(ticker, zacetek, konec)

    skupni_datumi = sorted(set(cene_izdelki["brent"]) & set(cene_izdelki["wti"]))


    vrstice = []

    for datum in skupni_datumi:
        vrstice.append({
            "datum": datum,
            "brent": cene_izdelki["brent"][datum],
            "wti": cene_izdelki["wti"][datum],
        })

    tabela = pd.DataFrame(vrstice)
    tabela["datum"] = pd.to_datetime(tabela["datum"])
    return tabela
    
def shrani(tabela, pot=output):
    tabela.to_csv(pot, index=False)
    print(f"Shranjenih {len(tabela)} vrstic v {pot}")

if __name__ == "__main__":
    nafta = zajemi_cene_nafte()
    shrani(nafta)
    