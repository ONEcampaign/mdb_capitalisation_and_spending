import pandas as pd
from oda_data import set_data_path, read_crs

from scripts import config
from scripts.logger import logger

set_data_path(config.Paths.raw_data)


def keep_study_mdbs(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only the list of MDBs in the config file. Deal with the European
    Investment Bank, which is an agency instead of a donor."""
    # Filter the data to keep only the MDBs
    df = df.loc[lambda d: d.donor_code.isin(config.MDBS)]

    # Keep only agency 3 for 918 (European Investment Bank)
    df = df.loc[
        lambda d: (d.donor_code != 918) | ((d.donor_code == 918) & (d.agency_code == 3))
    ]

    # Change donor name for agency 3 of 918 (European Investment Bank)
    df.loc[(df.donor_code == 918) & (df.agency_code == 3), "donor_name"] = (
        "European Investment Bank"
    )

    return df


def map_grants_non_grants(df: pd.DataFrame) -> pd.DataFrame:
    """Remap the oecd flow names as concessional and non-concessional loans,
    grants and equity investments."""
    # flow_name mapping
    flows = {
        "Other Official Flows (non Export Credit)": "Non-concessional loans",
        "ODA Grants": "Grants",
        "ODA Loans": "Concessional loans",
        "Equity Investment": "Equity investment",
    }

    # Map the flow names to the grants and non-grants categories
    df["flow_name"] = df.flow_name.map(flows)

    return df


def summarise_outflows_year_type(df: pd.DataFrame, grouper: list[str]) -> pd.DataFrame:
    """Summarise the outflows by year, donor and type of flow."""
    df = (
        df.groupby(by=grouper, observed=True, dropna=False, as_index=False)[
            ["usd_commitment", "usd_disbursement"]
        ]
        .sum()
        .sort_values(["year", "usd_disbursement"], ascending=[False, False])
    )

    return df


def add_mdb_total(df: pd.DataFrame, grouper: list[str]) -> pd.DataFrame:
    """Add a yearly total for the MDBs being studied."""
    df_total = (
        df.groupby(by=grouper, observed=True, dropna=False, as_index=False)[
            ["usd_commitment", "usd_disbursement"]
        ]
        .sum()
        .assign(donor_name="Total")
    )

    df = pd.concat([df, df_total], ignore_index=True)

    return df


def export_mdb_outflows(years: list[int] | range) -> None:
    """Pipeline function to get the data"""

    # get the data
    logger.info("Reading the data. If it needs downloading, this may take a while.")
    df = read_crs(years=years)

    # process the data
    logger.info("Processing the data")
    df = df.pipe(keep_study_mdbs).pipe(map_grants_non_grants)

    # Summarise the data by flow
    df_by_flow = df.pipe(
        add_mdb_total, grouper=["year", "donor_name", "flow_name"]
    ).pipe(summarise_outflows_year_type, grouper=["year", "donor_name", "flow_name"])

    df_summary = df_by_flow.pipe(add_mdb_total, grouper=["year", "donor_name"]).pipe(
        summarise_outflows_year_type, grouper=["year", "donor_name"]
    )

    # Save the data
    df_by_flow.to_csv(config.Paths.output / "mdb_outflows_by_flow.csv", index=False)
    logger.info("Data saved to mdb_outflows_by_flow.csv")

    df_summary.to_csv(config.Paths.output / "mdb_outflows_summary.csv", index=False)
    logger.info("Data saved to mdb_outflows_summary.csv")


if __name__ == "__main__":
    export_mdb_outflows(years=range(2010, 2023))
