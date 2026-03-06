"""Configuration settings for the entire project."""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_INTERIM = PROJECT_ROOT / "data" / "interim"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS_FIGURES = PROJECT_ROOT / "reports" / "figures"
REPORTS_EXCEL = PROJECT_ROOT / "reports" / "excel"

# File dictionaries
RAW_FILES = {
    'buyers': DATA_RAW / "buyer.csv",
    'sales': DATA_RAW / "sales.csv",
    'products_dir': DATA_RAW / "products"
}

CLEANED_FILES = {
    'buyers': DATA_INTERIM / "buyers_cleaned.csv",
    'sales': DATA_INTERIM / "sales_cleaned.csv",
    'products': DATA_INTERIM / "products_cleaned.csv"
}

MASTER_DATA = DATA_PROCESSED / "master_sales_data.csv"

# Business configuration
CONFIG = {
    "company_timezone": "America/Chicago",
    "shipping_flat_rate": 4.99,
    "black_friday_dates": ["2023-11-24", "2024-11-29", "2025-11-28"],
    "cost_per_staff_hour": 25,
    "sla_hours": 24,
    "min_staff_for_sla": 2,
    "referral_discount": 0.10,
    "referral_discount_black_friday": 0.20,
    "target_regions_2026": ["West", "Northeast"],
}
