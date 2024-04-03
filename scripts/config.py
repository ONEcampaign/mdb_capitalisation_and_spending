from pathlib import Path


class Paths:
    """Class to store the paths to the data and output folders."""

    project = Path(__file__).resolve().parent.parent
    raw_data = project / "raw_data"
    output = project / "output"
    scripts = project / "scripts"


MDBS = [
    913,  # African Development Bank (excluding African Development Fund)
    953,  # Arab Bank for Economic Development in Africa
    915,  # Asian Development Bank
    1024,  # Asian Infrastructure Investment Bank\
    981,  # Black Sea Trade and Development Bank
    906,  # Caribbean Development Bank
    910,  # Central American Bank for Economic Integration
    1013,  # Council of Europe Development Bank
    1015,  # Development Bank of Latin America
    990,  # European Bank for Reconstruction and Development
    918,  # European Investment Bank AGENCY CODE 3
    909,  # Inter-American Development Bank
    901,  # International Bank for Reconstruction and Development
    1037,  # International Investment Bank
    976,  # Islamic Development Bank
    # New Development Bank
    1045,  # North American Development Bank
]
