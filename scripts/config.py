from pathlib import Path


class Paths:
    """Class to store the paths to the data and output folders."""

    project = Path(__file__).resolve().parent.parent
    raw_data = project / "raw_data"
    output = project / "output"
    scripts = project / "scripts"


MDBS = {
    913: "African Development Bank",  # African Development Bank (excluding African Development Fund)
    953: "Arab Bank for Economic Development in Africa",  # Arab Bank for Economic Development in Africa
    915: "Asian Development Bank",  # Asian Development Bank
    1024: "Asian Infrastructure Investment Bank",  # Asian Infrastructure Investment Bank\
    981: "Black Sea Trade and Development Bank",  # Black Sea Trade and Development Bank
    906: "Caribbean Development Bank",  # Caribbean Development Bank
    910: "Central American Bank for Economic Integration",  # Central American Bank for Economic Integration
    1013: "Council of Europe Development Bank",  # Council of Europe Development Bank
    1015: "Development Bank of Latin America",  # Development Bank of Latin America
    990: "European Bank for Reconstruction and Development",  # European Bank for Reconstruction and Development
    918: "European Investment Bank",  # European Investment Bank AGENCY CODE 3
    909: "Inter-American Development Bank",  # Inter-American Development Bank
    901: "International Bank for Reconstruction and Development",  # International Bank for Reconstruction and Development
    1037: "International Investment Bank",  # International Investment Bank
    976: "Islamic Development Bank",  # Islamic Development Bank
    # New Development Bank
    1045: "North American Development Bank",  # North American Development Bank
}

AGENCIES = {
    46002: "African Development Bank",  # African Development Bank (excluding African Development Fund)
    # Arab Bank for Economic Development in Africa
    46004: "Asian Development Bank",  # Asian Development Bank
    46026: "Asian Infrastructure Investment Bank",  # Asian Infrastructure Investment Bank\
    46006: "Black Sea Trade and Development Bank",  # Black Sea Trade and Development Bank
    46009: "Caribbean Development Bank",  # Caribbean Development Bank
    46007: "Central American Bank for Economic Integration",  # Central American Bank for Economic Integration
    46024: "Council of Europe Development Bank",  # Council of Europe Development Bank
    46008: "Development Bank of Latin America",  # Development Bank of Latin America
    46015: "European Bank for Reconstruction and Development",  # European Bank for Reconstruction and Development
    46016: "European Bank for Reconstruction and Development",  # European Bank for Reconstruction and Development - Technical
    46017: "European Bank for Reconstruction and Development",  # European Bank for Reconstruction and Development - Technical
    46018: "European Bank for Reconstruction and Development",  # European Bank for Reconstruction and Development - Early T.
    46019: "European Bank for Reconstruction and Development",  # European Bank for Reconstruction and Development - Western B
    42004: "European Investment Bank",  # European Investment Bank AGENCY CODE 3
    46013: "Inter-American Development Bank",  # Inter-American Development Bank
    46012: "Inter-American Development Bank",  # Inter-American Development Bank
    44001: "International Bank for Reconstruction and Development",  # International Bank for Reconstruction and Development
    47146: "International Investment Bank",  # International Investment Bank
    46025: "Islamic Development Bank",  # Islamic Development Bank
    # New Development Bank
    # North American Development Bank
}
