from pathlib import Path

# On part du dossier racine du projet (lib est à la racine dans "lib/")
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
TXT_DIR = DATA_DIR / "fiches_produit_txt"
CSV_DIR = DATA_DIR / "fiches_produit_csv"

OUTPUT_DIR = PROJECT_ROOT / "output_data"
PRODUCTS_JSON_PATH = OUTPUT_DIR / "products_json" / "products.json"
PRODUCTS_CSV_PATH = OUTPUT_DIR / "products_csv" / "products.csv"
