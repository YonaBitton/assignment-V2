from __future__ import annotations

import json
from typing import Any, Dict, List

import pandas as pd
from loguru import logger

from lib.config import get_config
from lib.constants import PRODUCT_FIELDS
from lib.openai_client import client
from lib.utils import normalize_category, normalize_in_stock, normalize_price

_config = get_config()


def extract_product_from_text_with_openai(raw_text: str, raw_file: str) -> Dict[str, Any]:
    """Extrait un produit structuré à partir d'un texte brut de fiche produit."""
    system_msg = (
        "Tu es un assistant qui extrait des informations structurées de fiches produit. "
        "Tu dois répondre SEULEMENT avec un JSON valide, sans texte autour."
    )

    user_msg = f"""
Voici le contenu d'une fiche produit :

\"\"\"{raw_text}\"\"\"

Extrait les informations suivantes :

- product_name
- price (float, en euros)
- category
- colors (liste de couleurs)
- description_short (résumé en 1-2 phrases)
- features (liste de caractéristiques)
- in_stock (booléen)
- raw_file (nom du fichier), qui doit être: "{raw_file}"
"""

    response = client.chat.completions.create(
        model=_config["openai"]["model"],
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=_config["openai"]["temperature"],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    try:
        data: Dict[str, Any] = json.loads(content)
    except json.JSONDecodeError as exc:
        logger.error("Erreur de parsing JSON pour le fichier: {}", raw_file)
        logger.debug("Contenu renvoyé par le modèle :\n{}", content)
        raise exc

    for field in PRODUCT_FIELDS:
        data.setdefault(field, None)

    if data["colors"] is None:
        data["colors"] = []
    if data["features"] is None:
        data["features"] = []

    data["in_stock"] = normalize_in_stock(data["in_stock"])
    data["price"] = normalize_price(data["price"])
    data["category"] = normalize_category(data["category"])

    return data


def extract_products_from_txt_df(df_txt_raw: pd.DataFrame) -> pd.DataFrame:
    """Applique l'extraction OpenAI à tout un DataFrame de textes bruts."""
    products_txt: List[Dict[str, Any]] = []

    for _, row in df_txt_raw.iterrows():
        product = extract_product_from_text_with_openai(
            raw_text=row["raw_text"],
            raw_file=row["raw_file"],
        )
        products_txt.append(product)

    return pd.DataFrame(products_txt, columns=PRODUCT_FIELDS)
