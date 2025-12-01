# assignment-Levontin
# 🛒 Product Catalog Pipeline

An intelligent product catalog management system that extracts, validates, and normalizes product data from multiple sources (CSV & unstructured text files) using OpenAI, then exposes them through an interactive chatbot interface.

---

## ✨ Features

- **Multi-format Data Ingestion** — Load product data from structured CSV files and unstructured TXT files
- **AI-Powered Extraction** — GPT-based extraction from free-form text (configurable in `configs/base.yaml`)
- **Config-Driven Pipeline** — Centralized OpenAI, validation, and export settings
- **Data Validation** — Automatic validation rules (price > 0, allowed categories, required fields…)
- **Normalized Output** — Export clean, structured data (JSON + CSV)
- **Interactive Chatbot UI** — Ask questions in natural language about catalog products

---

## 📁 Project Structure
```
assignment-Levontin/
├── .env                      # Local environment variables (ignored)
├── .env.example              # Template for .env
├── configs/
│   ├── .gitkeep
│   └── base.yaml             # Main config: models, validation, export…
├── data/
│   ├── fiches_produit_csv/   # Raw CSV product files
│   └── fiches_produit_txt/   # Raw TXT product files
├── lib/
│   ├── __init__.py
│   ├── catalog.py            # Build prompt JSON for LLM
│   ├── chatbot.py            # Chatbot logic + system prompt
│   ├── config.py             # Loads YAML config
│   ├── constants.py          # Non-sensitive constants
│   ├── data_loading.py       # Load CSV/TXT into DataFrames
│   ├── export.py             # Save validated data to JSON/CSV
│   ├── openai_client.py      # OpenAI client wrapper
│   ├── parsing.py            # CSV normalization
│   ├── paths.py              # Path utilities
│   ├── text_extraction.py    # GPT-based text extraction
│   ├── ui_catalog_chat.py    # Panel dashboard for chatbot
│   ├── utils.py              # Helpers
│   └── validation.py         # Product validation rules
├── notebooks/
│   ├── clean_assignment.ipynb  # Main notebook
│   └── old_nb.ipynb
├── output_data/
│   ├── products_csv/
│   │   └── products.csv
│   └── products_json/
│       └── products.json
├── tests/                    # (empty placeholder for now)
├── .gitignore
├── Makefile
├── poetry.lock
├── pyproject.toml
└── README.md
````
---


## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- OpenAI API key


### Installation

```bash
# Clone the repository
git clone <repo-url>
cd assignment-Levontin

# Install dependencies with Poetry
make install

# Or manually:
poetry install
```


---

## 🔐 Environment Setup

Create a `.env` file at the project root:

```env
OPENAI_API_KEY=your-openai-api-key-here
```
Edit the example file
```bash
cp .env.example .env
```

---

## 📖 Usage

### 1. Run the Notebook Pipeline

Open and run the Jupyter notebook to process the full pipeline:

```bash
poetry run jupyter lab notebooks/clean_assignment.ipynb
```

The notebook will:
1. Load products from CSV and TXT files
2. Extract structured data from text using OpenAI
3. Normalize and merge all products
4. Validate products against business rules
5. Export to `output_data/`

---

### 2. Interactive Chatbot

After processing, launch the chatbot UI to query your catalog:

```python
from lib.catalog import build_catalog_for_llm
from lib.chatbot import create_catalog_system_context
from lib.ui_catalog_chat import build_catalog_chat_dashboard

# Build context from your validated DataFrame
catalog_text = build_catalog_for_llm(df_validated)
context = create_catalog_system_context(catalog_text)

# Launch dashboard
dashboard = build_catalog_chat_dashboard(context)
dashboard
```

Ask things like:

- *« Quels produits y a-t-il dans la catégorie wearable ? »*
- *« Donne-moi les détails sur la chaise de bureau »*
- *“Summarize in one sentence the office chair”*
- *“Which products are suitable for remote work?”*

---

## ✅ Validation Rules
Products are validated against the following rules:

| Field | Rule |
|-------|------|
| `price` | Must be a positive number |
| `category` | Must be in allowed list (furniture, electronics, wearable, etc.) |
| `product_name` | Cannot be empty |
| `description_short` | Max 280 characters |
| `in_stock` | Must be a boolean |
| `features` | If present, must be a non-empty list |

### Allowed Categories

- `furniture`
- `electronics`
- `electronics / audio`
- `electronics / lighting`
- `accessory`
- `wearable`
- `office`
- `clothing`
---

## 🛠️ Development

### Tests (empty for now)

```bash
make test
# or
poetry run pytest
```

### Format & Lint Code

If `make` doesn't work on your environment:

```bash
poetry run pre-commit run --all-files
```

Runs ruff, codespell, nbstripout, etc.

---

## 📦 Main Dependencies

| Package        | Purpose |
|----------------|---------|
| pandas         | Data manipulation |
| openai         | GPT API |
| panel          | Dashboard UI |
| python-dotenv  | Environment loading |
| loguru         | Logging |
| pytest         | Testing |
| pre-commit     | Code quality |

See `pyproject.toml` for the complete list.
---

## 📄 License

Project for assignment purposes.

---

## 👤 Author

**Yona Bitton** — yonabitton@gmail.com
