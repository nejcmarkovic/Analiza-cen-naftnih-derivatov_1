# Tukaj zajamemo podatke o maloprodajnih cenah naftnih derivatov v Sloveniji.
# Te podatke jemljemo s portala energetika.

import re
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = ( "https://www.energetika-portal.si/podrocja/energetika/"
    "cene-naftnih-derivatov/regulirane-cene-naftnih-derivatov/" )

output = "data/raw/si_cene_derivatov.csv"

def prenesi_stran(url=URL):
    odziv = requests.get(url, timeout=10)
    odziv.raise_for_status()
    return odziv.text

def pretvori_datum(niz):
    niz = niz.strip()
    if not re.match(r"^\d{1,2}\.\d{1,2}\.\d{4}$", niz):
        return None
    return datetime.strptime(niz, "%d.%m.%Y").strftime("%Y-%m-%d")


def pretvori_v_stevilo(niz):
    niz = niz.strip()
    if niz in ("", "/") or "cene" in niz.lower():
        return None
    if not re.match(r"^\d+,\d+$", niz):
        return None
    return float(niz.replace(",","."))
def zajemi_cene(url=URL):
    html = prenesi_stran(url)
    juha = BeautifulSoup(html, "html.parser")
    tabela_html = juha.find("table")

    vrstice = []

    for vrstica in tabela_html.find_all("tr"):
        celice = [celica.get_text(strip=True) for celica in vrstica.find_all("td")]
        if len(celice) < 4:
            continue

        datum = pretvori_datum(celice[0])
        if datum is None:
            continue
        vrstice.append({"datum": datum, "bencin_95": pretvori_v_stevilo(celice[1]), "dizel": pretvori_v_stevilo(celice[2]),
            "kurilno_olje": pretvori_v_stevilo(celice[3])})
    tabela = pd.DataFrame(vrstice)
    tabela["datum"] = pd.to_datetime(tabela["datum"])
    tabela = tabela.sort_values("datum").reset_index(drop=True)
    return tabela

def shrani(tabela, pot=output):
    tabela.to_csv(pot, index = False)
    print(f"Shranjenih {len(tabela)} vrstic v {pot}")

if __name__ == "__main__":
    cene = zajemi_cene()
    shrani(cene)

