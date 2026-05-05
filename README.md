# canarias-analisis

Open data analysis of the Gobierno de Canarias (ISTAC).

Datasets from [datos.canarias.es](https://datos.canarias.es) — CKAN portal of the Instituto Canario de Estadística.

## Structure

```
canarias-analisis/
├── README.md
├── PROCEDURE.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── 01_incidentes_stradales.ipynb
│   └── 02_vivienda_prezzi.ipynb
├── src/
│   └── fetch.py
├── data/
│   └── raw/                     # gitignored — download fresh each time
└── output/
    └── figures/
```

## Topics available

| # | Topic | Description | Period |
|---|---|---|---|
| 01 | Road accidents | Deaths by province and road type | 1999–2023 |
| 02 | Housing prices | Index (base 2015=100) — Canary Islands vs Spain | 2007–2025 |
| 03 | Unemployment | Beneficiaries, coverage rate, registered unemployed | 2000–2026 |
| 04 | Vacational rentals | 73k registered properties across islands and municipalities | live registry |
| 05 | Airport flights | Commercial operations by island — Gran Canaria vs Tenerife | 2004–2020 |

## Setup

```bash
pip install -r requirements.txt
```

## Adding a new topic

See [PROCEDURE.md](./PROCEDURE.md) for the standard workflow.