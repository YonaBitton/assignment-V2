from __future__ import annotations

from typing import Optional

import pandas as pd

# common normalization to both txt and csv files


def normalize_price(value: int | float | str | None) -> Optional[float]:
    """Convertit un prix en float.

    Gère les formats : '129', '129.0', '129,99', '129 €', '129 euros', etc.
    Retourne None si la valeur est vide ou non convertible.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip().lower()
    s = s.replace("€", "").replace("eur", "").replace("euros", "").replace("euro", "")
    s = s.replace(",", ".").strip()

    return float(s) if s else None


def normalize_in_stock(value: bool | str | int | float | None) -> bool:
    """Convertit une valeur de stock en booléen.

    Retourne False si 'rupture' ou 'épuisé' est détecté.
    Retourne True par défaut (stock disponible).
    """
    if isinstance(value, bool):
        return value

    s = str(value).lower()

    if "rupture" in s or "épuisé" in s:
        return False

    return True
