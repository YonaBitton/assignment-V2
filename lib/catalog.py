from __future__ import annotations

import json
from typing import Any, Dict, List

import pandas as pd


def build_catalog_for_llm(df: pd.DataFrame) -> str:
    """Construit une représentation JSON du catalogue à partir d'un DataFrame.

    Chaque ligne devient un produit avec les champs :
    - id
    - name
    - category
    - price_eur
    - colors
    - description
    - features
    - in_stock
    """
    products: List[Dict[str, Any]] = []

    for idx, row in df.iterrows():
        products.append(
            {
                "id": int(idx),
                "name": row["product_name"],
                "category": row["category"],
                "price_eur": row["price"],
                "colors": row["colors"],
                "description": row["description_short"],
                "features": row["features"],
                "in_stock": row["in_stock"],
            }
        )

    return json.dumps(products, ensure_ascii=False, indent=2)
