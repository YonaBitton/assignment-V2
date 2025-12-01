from pathlib import Path

import pandas as pd
import re



def load_csv_products(csv_dir: Path) -> pd.DataFrame:
    """Charge tous les fichiers CSV produits et les concatène."""
    csv_paths = sorted(csv_dir.glob("*.csv"))

    frames: list[pd.DataFrame] = []
    for path in csv_paths:
        products_df = pd.read_csv(path)
        products_df["raw_file"] = path.name
        frames.append(products_df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def load_txt_products(txt_dir: Path) -> pd.DataFrame:
    """Charge tous les fichiers TXT produits dans un DataFrame (texte brut).

    Si un fichier contient plusieurs fiches séparées par des lignes '---',
    chaque bloc est traité comme une fiche produit distincte.
    """
    txt_paths = sorted(txt_dir.glob("*.txt"))
    records: list[dict[str, str]] = []

    for path in txt_paths:
        full_text = path.read_text(encoding="utf-8")

        # on découpe sur des lignes contenant seulement des tirets (---)
        blocks = re.split(r"\n-{3,}\n", full_text)
        blocks = [b.strip() for b in blocks if b.strip()]

        if len(blocks) <= 1:
            # cas normal : 1 fichier = 1 produit
            records.append(
                {
                    "raw_file": path.name,
                    "raw_text": full_text,
                }
            )
        else:
            # cas multi-produits : 1 fichier = plusieurs fiches
            for i, block in enumerate(blocks, start=1):
                records.append(
                    {
                        # on garde trace du fichier + numéro de bloc
                        "raw_file": f"{path.name}#part{i}",
                        "raw_text": block,
                    }
                )

    return pd.DataFrame(records)
