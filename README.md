#  MDB inflows and outflows data
This repository contains simple scripts to get inflows and outflows data for major MDBs.
It uses data from the OECD Creditor Reporting System (CRS) and the Members Use of the Multilateral
System databases. 

## Reproducing the analysis
To reproduce the analysis, you need python 3.11 or higher. You also need to install
a few dependencies, using poetry.

```bash
poetry install
```

### Outflows
To export the outflows data, you can run the [outflows.py](/scripts/outflows.py) script. This will download
the required data from the OECD, store it in the `raw_data` folder, and save the
outputs in the `outflows` folder.

From the main repository directory, run:

```bash
poetry run python scripts/outflows.py
```

You can also just run the script in a python terminal.

### Inflows
To export the inflows data, you can run the [inflows.py](/scripts/inflows.py) script. This will download
the required data from the OECD, store it in the `raw_data` folder, and save the
outputs in the `inflows` folder.

From the main repository directory, run:

```bash
poetry run python scripts/inflows.py
```

You can also just run the script in a python terminal.

## Notes on the analysis
The scripts on this repository filter the CRS data for a list of MDBs which can be found
in the [config.py](scripts/config.py) file. Note there is no data for the New Development Bank
and data is not available for every MDB for every year.

We map the types of (out)flows based on the OECD's breakdown of concessional and non-concessional
flows. In this context, we have broken it down by concessional and non-concessional loans,
grants, and equity investments. This mapping can be tweaked in the [outflows.py](scripts/outflows.py)
file, inside the `map_grants_non_grants` function.

The data is presented as USD millions of commitments and disbursements in nominal prices.
We can easily convert to constant prices or other currencies if needed.


