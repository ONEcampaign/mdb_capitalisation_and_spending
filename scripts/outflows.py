import pandas as pd
from oda_data import set_data_path, read_crs

from scripts import config

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


def summarise_outflows_year_type(df: pd.DataFrame) -> pd.DataFrame:
    """Summarise the outflows by year, donor and type of flow."""
    df = (
        df.groupby(
            [
                "year",
                "donor_name",
                "flow_name",
            ],
            observed=True,
            dropna=False,
            as_index=False,
        )[["usd_commitment", "usd_disbursement"]]
        .sum()
        .sort_values(["year", "usd_disbursement"], ascending=[False, False])
    )

    return df


def add_mdb_total(df: pd.DataFrame) -> pd.DataFrame:
    """Add a yearly total for the MDBs being studied."""
    df_total = (
        df.groupby(
            [
                "year",
                "flow_name",
            ],
            observed=True,
            dropna=False,
            as_index=False,
        )[["usd_commitment", "usd_disbursement"]]
        .sum()
        .assign(donor_name="Total")
    )

    df = pd.concat([df, df_total], ignore_index=True)

    return df


def get_mdb_outflows(years: list[int] | range) -> pd.DataFrame:
    """Pipeline function to get the data"""
    df = (
        read_crs(years=years)
        .pipe(keep_study_mdbs)
        .pipe(map_grants_non_grants)
        .pipe(add_mdb_total)
        .pipe(summarise_outflows_year_type)
    )

    return df


if __name__ == "__main__":
    data = get_mdb_outflows(years=range(2010, 2023))
