# canarias-analisis

Open data analysis of the Gobierno de Canarias (ISTAC).

Datasets from [datos.canarias.es](https://datos.canarias.es) — CKAN portal of the Instituto Canario de Estadística.

## Structure

```
canarias-analisis/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── 01_incidentes_stradales.ipynb
├── src/
│   └── fetch.py
└── output/
    └── figures/
```

## Topics available

- **Road accidents** — mortality by province and road type, 1999–2023

## Setup

```bash
pip install -r requirements.txt
```

## Notebooks

| # | Topic | Data |
|---|---|---|
| 01 | Road accidents | Deaths by province and road type, 1999–2023 |

To add a topic: `src/fetch.py` downloads CSVs from CKAN, `notebooks/` contains the analysis.