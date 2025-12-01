from pathlib import Path

import pandas as pd


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
    """Charge tous les fichiers TXT produits dans un DataFrame (texte brut)."""
    txt_paths = sorted(txt_dir.glob("*.txt"))
    records: list[dict[str, str]] = []

    for path in txt_paths:
        text = path.read_text(encoding="utf-8")
        records.append(
            {
                "raw_file": path.name,
                "raw_text": text,
            }
        )

    return pd.DataFrame(records)
