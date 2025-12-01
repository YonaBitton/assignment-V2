from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from lib.config import get_config
from lib.constants import ALLOWED_CATEGORIES

_config = get_config()


def validate_product(product: Dict[str, Any]) -> Dict[str, Any]:  # noqa: C901
    """Vérifie qu'un produit respecte les règles de validation.

    Retourne un dict avec :
      - validation_status: "ok" ou "error"
      - validation_errors: liste de messages d'erreurs.
    """
    errors: List[str] = []

    # price > 0
    price = product.get("price")
    if not isinstance(price, (int, float)) or price <= 0:
        errors.append("price must be a positive number")

    # category dans une liste autorisée
    category_raw = product.get("category")
    category = (category_raw or "").strip().lower()
    if not category:
        errors.append("category is missing")
    elif category not in ALLOWED_CATEGORIES:
        errors.append(f"category '{category}' is not allowed")

    # product_name non vide
    name = (product.get("product_name") or "").strip()
    if not name:
        errors.append("product_name is empty")

    # description_short ≤ max_description_length caractères
    max_desc_length = _config["validation"]["max_description_length"]
    desc = product.get("description_short") or ""
    if len(desc) == 0:
        errors.append("description_short is empty")
    elif len(desc) > max_desc_length:
        errors.append(f"description_short exceeds {max_desc_length} characters")

    # in_stock booléen
    in_stock = product.get("in_stock")
    if not isinstance(in_stock, bool):
        errors.append("in_stock must be a boolean")

    # features liste non vide si présente
    features = product.get("features")
    if features is not None:
        if not isinstance(features, list):
            errors.append("features must be a list if present")
        elif len(features) == 0:
            errors.append("features list is empty")

    status = "ok" if not errors else "error"

    return {
        "validation_status": status,
        "validation_errors": errors,
    }


def add_validation_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Applique validate_product à chaque ligne et ajoute les colonnes de validation."""
    df_validated = df.copy()
    validation = df_validated.apply(
        lambda row: validate_product(row.to_dict()),
        axis=1,
        result_type="expand",
    )

    df_validated[["validation_status", "validation_errors"]] = validation

    return df_validated
