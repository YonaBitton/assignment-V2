from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

import pandas as pd
from loguru import logger

from lib.config import get_config
from lib.constants import CSV_COLUMNS
from lib.paths import PRODUCTS_CSV_PATH, PRODUCTS_JSON_PATH

_config = get_config()


def make_products_json(df: pd.DataFrame) -> str:
    """Retourne une chaîne JSON indentée contenant toutes les colonnes du DataFrame."""
    records = df.to_dict(orient="records")
    return json.dumps(records, ensure_ascii=False, indent=_config["export"]["json_indent"])


def make_products_csv_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne un DataFrame ne contenant que les colonnes nécessaires pour le CSV.

    Vérifie que toutes les colonnes de `CSV_COLUMNS` sont présentes dans `df`.
    """
    missing = [col for col in CSV_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le DataFrame : {missing}")

    return df[CSV_COLUMNS].copy()


def export_products(df_validated: pd.DataFrame) -> Tuple[Path, Path]:
    """Exporte les produits validés en JSON complet + CSV filtré.

    - Génère le JSON complet et le CSV filtré à partir de `df_validated`.
    - Crée les dossiers si nécessaire.
    - Écrit :
        * products.json dans output_data/products_json/
        * products.csv dans output_data/products_csv/
    - Affiche les chemins générés.
    - Retourne (json_path, csv_path).
    """
    json_str = make_products_json(df_validated)
    csv_frame = make_products_csv_frame(df_validated)

    PRODUCTS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    PRODUCTS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    encoding = _config["export"]["csv_encoding"]
    PRODUCTS_JSON_PATH.write_text(json_str, encoding=encoding)
    csv_frame.to_csv(PRODUCTS_CSV_PATH, index=False, encoding=encoding)

    logger.success("JSON exporté vers : {}", PRODUCTS_JSON_PATH)
    logger.success("CSV exporté vers  : {}", PRODUCTS_CSV_PATH)

    return PRODUCTS_JSON_PATH, PRODUCTS_CSV_PATH
