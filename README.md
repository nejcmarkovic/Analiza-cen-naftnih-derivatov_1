# Analiza cen naftnih derivatov

Projektna naloga pri predmetu Uvod v programiranje. Program zajame podatke o
reguliranih maloprodajnih cenah naftnih derivatov v Sloveniji (bencin NMB-95,
dizel, kurilno olje) s [Portala Energetika](https://www.energetika-portal.si/podrocja/energetika/cene-naftnih-derivatov/regulirane-cene-naftnih-derivatov/),
jih primerja s svetovno ceno surove nafte (Brent, WTI) prek javnega JSON
vmesnika Yahoo Finance, ter s cenami goriva v Avstriji in Italiji prek
uradne EU tabele (Weekly Oil Bulletin, Evropska komisija). Nato izvede
statistično analizo (korelacija, drseča povprečja, volatilnost, primerjava
med državami) in vizualizacijo podatkov.

## Struktura projekta

- `src/scraper.py` – Zajame zgodovinske cene goriva v Sloveniji s Portala Energetika (BeautifulSoup + regularni izrazi).
- `src/fetch_oil.py` – Zajame zgodovinske svetovne cene surove nafte (Brent, WTI) prek Yahoo Finance.
- `src/proces.py` – Obdela surove podatke: poravna jih na dnevni nivo in ju združi v eno tabelo.
- `src/analiza1.py` – Izračuna statistične kazalnike: korelacijo, drseča povprečja, volatilnost.
- `src/fetch_eu.py` – Zajame cene goriva za Slovenijo, Avstrijo in Italijo iz uradne EU tabele.
- `src/primerjava.py` – Primerja cene med državami (povprečja, razlike do Slovenije, korelacije).
- `analiza.ipynb` – Jupyter zvezek, ki poveže vse zgornje korake in prikaže analizo z grafi.
- `data/` – Mapa s shranjenimi podatki (`raw/` – surovi podatki, `processed/` – obdelani, združeni podatki).
- `uporaba-ui.md` – Dokumentacija uporabe orodij umetne inteligence pri nastajanju projekta.

## Namestitev

1. **Ustvarite in aktivirajte virtualno okolje:**
```bash
   python3 -m venv venv
   source venv/bin/activate
```
   (na Windows: `venv\Scripts\activate`)

2. **Namestite potrebne knjižnice:**
```bash
   pip3 install -r requirements.txt
```

## Zagon

Odprite `analiza.ipynb` (npr. v VS Code ali prek `jupyter notebook`) in
poženite celice od zgoraj navzdol (Run → Restart Kernel and Run All Cells).
Notebook sam pokliče zajem podatkov, obdelavo in izriše grafe analize –
ni potrebno poganjati posameznih `.py` datotek ročno.

## Podatki

- Slovenske regulirane cene goriva: [Portal Energetika](https://www.energetika-portal.si/podrocja/energetika/cene-naftnih-derivatov/regulirane-cene-naftnih-derivatov/)
- Svetovne cene nafte (Brent/WTI): javni JSON vmesnik [Yahoo Finance](https://finance.yahoo.com/)
- Cene goriva v Avstriji in Italiji: [Weekly Oil Bulletin, Evropska komisija](https://energy.ec.europa.eu/)

## Opombe o podatkih

- Za obdobje avgust–september 2020 so bile cene bencina in dizla v Sloveniji
  fiksirane na 1,000 EUR/l, kurilno olje pa v tem obdobju ni bilo regulirano
  (manjkajoče vrednosti v podatkih za ta čas).
- Primerjava držav je omejena na Slovenijo, Avstrijo in Italijo, ker imajo
  vse tri v celotnem obravnavanem obdobju evro kot valuto (izognemo se
  dodatni pretvorbi prek menjalnega tečaja).