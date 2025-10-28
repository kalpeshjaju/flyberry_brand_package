# Flyberry Brand Package Generator

**Purpose**: Generate HTML brand documentation from structured JSON data

## Quick Start

```bash
# Build all HTML files
python3 build.py

# View output
open docs/index.html
```

## Structure

```
flyberry_brand_package/
├── build.py                    # Main build script
├── data_integration.py         # Data source connector
├── data/ -> ../flyberry_oct_restart  # Data source
├── generators/                 # HTML generators
├── source/                     # Markdown sources
├── templates/                  # HTML templates
├── assets/                     # CSS and images
└── docs/                       # Generated HTML output
```

## Data Source

This project reads data from `flyberry_oct_restart/` via symlink.
All product data, recipes, and brand information comes from structured JSON files.

## Requirements

- Python 3.8+
- `markdown` package (`pip install markdown`)
- Data source: `../flyberry_oct_restart/`

## Building

1. Ensure data source exists at `../flyberry_oct_restart/`
2. Run: `python3 build.py`
3. Output will be in `docs/` directory

## Validation

Run validation before commits:
```bash
python3 generators/anti_hallucination_validator.py
```

---
Generated: $(date +%Y-%m-%d)
