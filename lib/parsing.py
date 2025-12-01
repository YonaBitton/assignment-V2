# lib/parsing.py

from __future__ import annotations

import re
from typing import Dict, List

import pandas as pd

from lib.constants import PRODUCT_FIELDS
from lib.utils import normalize_in_stock, normalize_price


def parse_colors(value: object | None) -> List[str]:
    """Convertit une chaîne de couleurs en liste normalisée."""
    if value is None or pd.isna(value):
        return []

    s = str(value).lower()
    parts = re.split(r"[,/;]|et", s)
    return [p.strip() for p in parts if p.strip()]


def parse_features(value: object | None) -> List[str]:
    """Convertit une chaîne de features en liste."""
    if value is None or pd.isna(value):
        return []

    s = str(value)
    parts = re.split(r"[;•\n\-]+", s)
    return [p.strip() for p in parts if p.strip()]


def normalize_csv_products(df_csv: pd.DataFrame) -> pd.DataFrame:
    """Transforme le df brut CSV en tableau standardisé."""
    products: List[Dict[str, object]] = []

    for _, row in df_csv.iterrows():
        product: Dict[str, object] = {
            "product_name": str(row.get("product_name", "")).strip(),
            "price": normalize_price(row.get("price")),
            "category": str(row.get("category", "")).strip().lower(),
            "colors": parse_colors(row.get("colors")),
            "description_short": str(row.get("description", "")).strip(),
            "features": parse_features(row.get("features")),
            "in_stock": normalize_in_stock(row.get("stock", "")),
            "raw_file": row.get("raw_file"),
        }
        products.append(product)

    return pd.DataFrame(products, columns=PRODUCT_FIELDS)
