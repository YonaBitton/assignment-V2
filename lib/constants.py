from typing import Final, List

PROJECT_ID = "assignment-levontin"


PRODUCT_FIELDS: Final[List[str]] = [
    "product_name",
    "price",
    "category",
    "colors",
    "description_short",
    "features",
    "in_stock",
    "raw_file",
]


ALLOWED_CATEGORIES = {
    "furniture",
    "electronics",
    "electronics / audio",
    "electronics / lighting",
    "accessory",
    "wearable",
    "office",
    "clothing",
}


CSV_COLUMNS: List[str] = [
    "product_name",
    "price",
    "category",
    "in_stock",
    "validation_status",
]
