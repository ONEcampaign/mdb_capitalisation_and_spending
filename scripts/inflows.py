import pandas as pd
from oda_data import set_data_path, read_multisystem

from scripts import config
from scripts.logger import logger


set_data_path(config.Paths.raw_data)


def keep_core_contributions(df: pd.DataFrame) -> pd.DataFrame:
    """Filter data to keep only core contributions"""

    df = df.loc[lambda d: d.aid_to_or_thru == "Core contributions to"]

    return df


def keep_study_agencies(df: pd.DataFrame) -> pd.DataFrame:
    """Filter data to keep only the agencies in the config file."""

    # Filter agency codes
    df = df.loc[lambda d: d.channel_code.isin(config.AGENCIES)].copy()

    # Map names to codes
    df["channel_name"] = df.channel_code.map(config.AGENCIES)

    return df


def group_by_donor_mdb(df: pd.DataFrame) -> pd.DataFrame:
    """Group the data by donor, channel and flow type."""
    df = df.groupby(
        ["year", "donor_name_e", "channel_name", "flow_type"],
        observed=True,
        dropna=False,
        as_index=False,
    )["amount"].sum()

    return df


def export_core_contributions_providers(df: pd.DataFrame) -> None:
    """Export the list of providers of core contributions."""
    df = df[["donor_name_e"]].drop_duplicates().sort_values("donor_name_e")

    df.to_csv(config.Paths.output / "core_contributions_providers.csv", index=False)

    return df


def group_by_mdb(df: pd.DataFrame) -> pd.DataFrame:
    """Group the data by year, channel and flow type."""
    df = df.groupby(
        ["year", "channel_name", "flow_type"],
        observed=True,
        dropna=False,
        as_index=False,
    )["amount"].sum()

    return df


def pivot_flow(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot the flow data to have the flow types as columns."""
    df = df.pivot(
        index=["year", "channel_name"],
        columns="flow_type",
        values="amount",
    )

    return df.reset_index()


def add_mdb_total(df: pd.DataFrame, column_name: str = "channel_name") -> pd.DataFrame:
    """Add a yearly total for the MDBs being studied."""
    df_total = (
        df.groupby(by=["year", "channel_name"], observed=True, dropna=False)[
            ["Commitments", "Disbursements"]
        ]
        .sum()
        .reset_index()
    )

    df_total[column_name] = "Total"

    df = pd.concat([df, df_total], ignore_index=True)

    return df


def export_mdb_inflows(years: list[int] | range) -> None:
    """Pipeline function to get the data"""

    # get the data
    logger.info("Reading the data. If it needs downloading, this may take a while.")
    df = read_multisystem(years=years)

    # process the data
    logger.info("Processing the data")
    df = (
        df.pipe(keep_core_contributions)
        .pipe(keep_study_agencies)
        .pipe(group_by_donor_mdb)
    )

    # export providers list
    export_core_contributions_providers(df)

    # summarise the data by mdb and pivot the flow
    df = df.pipe(group_by_mdb).pipe(pivot_flow)

    # Add mdb total
    df = add_mdb_total(df, column_name="channel_name")

    # Save the data
    df.to_csv(config.Paths.output / "mdb_inflows.csv", index=False)
    logger.info("Data saved to mdb_inflows.csv")


if __name__ == "__main__":
    export_mdb_inflows(range(2010, 2023))
