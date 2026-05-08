# Adding a new topic — fixed workflow

```bash
# 1. Find a dataset on datos.canarias.es
curl "https://datos.canarias.es/catalogos/general/api/action/package_search?q=<keyword>&rows=5"

# 2. Download + auto-rename (es. 1.4.csv -> indice-de-precios-de-vivienda.csv)
python -m src.fetch --dataset <package_name> --output data/raw/

# 3. Create notebooks/<NN>_<topic>.ipynb
#    Cell 0 (markdown): title, source link, question
#    Cell 1 (code):     load + print shape (CWD guard already there)
#    Cell 2 (code):     normalize (types, names, filter)
#    Cells 3-5 (code):  analysis — exactly 3 plots
#    Last cell (code):  key numbers table

# 4. Execute (kernel runs in project_root — CWD guard handles it)
jupyter nbconvert --to notebook --execute notebooks/<NN>_<topic>.ipynb --output-dir notebooks/

# 5. Verify figures are in output/figures/<topic>_*.png

# 6. Update README: add row to "Topics available" table

# 7. Update PROCEDURE.md: add dataset ID to "Useful dataset IDs" table

# 8. Commit
git add notebooks/<NN>_<topic>.ipynb output/figures/<topic>*.png README.md PROCEDURE.md
git commit -m "<NN> — <topic>: short description

- Dataset: <source> (<org>, <year_range>)
- <n> figures: <list>
- Note: data/raw/ is gitignored — download fresh before running"
git push
```

## Conventions

| Item | Rule |
|---|---|
| Language | English |
| Notebook naming | `01_<topic>.ipynb`, `02_<topic>.ipynb` |
| Figure names | `<topic>_<description>.png` |
| Data | Gitignored — download fresh each time |
| Data format | CSV preferred over PC-Axis, JSON, PDF |
| Series length | ≥ 5 years preferred |
| Plots | Exactly 3 per notebook |

## Notes on `src/fetch.py`

Auto-renames downloaded files to human-readable names. Pass `--no-rename` to disable. Counter appended if file exists.

## Useful dataset IDs

| Topic | Dataset name |
|---|---|
| Road accidents | `accidentes-de-circulacion-con-victimas-mortales-por-lugar-del-accidente-provincias-de-canarias-1` |
| Housing prices | `indice-de-precios-de-vivienda-segun-el-orden-de-transmision-de-la-vivienda-espana-y-comuni-2015` |
| Unemployment benefits | `indicadores-de-prestaciones-por-desempleo-canarias-y-provincias-por-periodos` |
| Tourist accommodation | `establecimientos-extrahoteleros-de-tipologia-vivienda-vacacional-inscritos-en-el-registro` |
| Airport flights | `operaciones-en-las-islas-de-canarias-segun-movimientos-servicios-y-territorios-de-origen-destin` |
| Tourism employment | `empresas-segun-actividades-turisticas-cnae-09-islas-de-canarias-y-periodos1` |
| Tourist digital behavior | `turistas-de-16-y-mas-anos-segun-si-han-usado-en-canarias-un-smartphone-o-tablet-con-conexion-a-internet-2-2` |
| Water consumption | `volumen-y-volumen-por-habitante-y-dia-de-agua-segun-ciclos-del-agua-canarias-por-anos` |
| GDP | `principales-resultados-del-pib-comunidades-autonomas-por-anos-desde-20001` |
| Foreign trade | (to find) |
