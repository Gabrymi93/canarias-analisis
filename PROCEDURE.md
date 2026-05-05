# Adding a new topic to canarias-analisis

This document describes the standard workflow for adding a new analysis notebook.

---

## 1. Discover

Search the CKAN catalog for a topic via HTTP:

```bash
curl "https://datos.canarias.es/catalogos/general/api/action/package_search?q=<keyword>&rows=5&sort=metadata_modified desc"
```

Browse by category: empleo, turismo, vivienda, demografia, transporte, salud...

Key criteria for selection:
- **CSV resource available** (not only PDF/PC-Axis/API)
- **Series ≥ 5 years** of historical data
- **Province-level granularity** preferred (island or province breakdown)

Check the dataset via `package_show` to confirm resources and formats:
```bash
curl "https://datos.canarias.es/catalogos/general/api/action/package_show?id=<package_name>"
```

---

## 2. Download

```bash
python -m src.fetch --dataset <package_name> --output data/raw/
```

File is saved to `data/raw/`. The raw data directory is **gitignored** — always re-download to keep the analysis reproducible.

---

## 3. Explore

Create a new notebook:
```
notebooks/<nn>_<topic>.ipynb
```

Notebook structure per topic:
- **Cell 0** (markdown): title, source link, research question in 1-2 sentences
- **Cell 1** (code): load data + print shape
- **Cell 2** (code): normalize — types, column names, filter valid rows
- **Cells 3+** (code): analysis — 2 to 3 plots maximum per notebook
- **Last cell** (code): key numbers summary table

**Figure naming**: `<topic>_<description>.png`
**Output directory**: `output/figures/`

---

## 4. Execute and verify

```bash
jupyter nbconvert --to notebook --execute notebooks/<nn>_<topic>.ipynb --output-dir .
```

Check that figures are written to `output/figures/` before committing.

---

## 5. Update documentation

Before committing, update:

- **`README.md`** — add the new notebook to the table in the Notebooks section:
  ```markdown
  | <nn> | <Topic> | <Short description> (<years>) |
  ```
- **`data/raw/.gitkeep`** — keep directory tracked (empty placeholder is fine)

---

## 6. Commit and push

```bash
git add notebooks/<nn>_<topic>.ipynb \
         output/figures/<topic>*.png \
         README.md

git commit -m "<nn> — <topic>: short description

- Dataset: <source> (<org>, <year_range>)
- <n> figures: <list>
- Note: data/raw/ is gitignored — download fresh before running"

git push
```

---

## 7. Update PROCEDURE.md

After adding a new topic, check whether the procedure itself needs an update (e.g., new conventions added, edge cases documented). If something changed, update this file in the same commit.

---

## Notes on `src/fetch.py`

The fetch script automatically renames downloaded files to human-readable names
(e.g. `1.4.csv` → `indice-de-precios-de-vivienda.csv`) unless you pass `--no-rename`.

If a file already exists with that name, it appends a counter (`_1`, `_2`, ...).

---

## Conventions summary

| Item | Rule |
|---|---|
| Language | Everything in English |
| Notebook naming | `01_<topic>.ipynb`, `02_<topic>.ipynb`, ... |
| Figure names | `<topic>_<description>.png` |
| Data | Gitignored — download fresh each time |
| Data format | CSV preferred over PC-Axis, JSON, PDF |
| Series length | ≥ 5 years preferred |
| Plots per notebook | 2-3 maximum |

---

## Useful dataset IDs

| Topic | Dataset name |
|---|---|
| Road accidents | `accidentes-de-circulacion-con-victimas-mortales-por-lugar-del-accidente-provincias-de-canarias-1` |
| Housing prices | `indice-de-precios-de-vivienda-segun-el-orden-de-transmision-de-la-vivienda-espana-y-comuni-2015` |
| Unemployment benefits | `indicadores-de-prestaciones-por-desempleo-canarias-y-provincias-por-periodos` |
| Tourist accommodation | `establecimientos-extrahoteleros-de-tipologia-vivienda-vacacional-inscritos-en-el-registro` |