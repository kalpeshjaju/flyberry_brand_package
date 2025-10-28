#!/bin/bash

# Flyberry Brand Package Cleanup Script
# Purpose: Archive non-essential files to create a clean production structure
# Date: 2025-10-24
# Usage: bash cleanup.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Flyberry Brand Package Cleanup Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Create archive directory with timestamp
ARCHIVE_DIR="_archive_$(date +%Y-%m-%d_%H-%M-%S)"
echo -e "${YELLOW}Creating archive directory: $ARCHIVE_DIR${NC}"
mkdir -p "$ARCHIVE_DIR"
mkdir -p "$ARCHIVE_DIR/generators"
mkdir -p "$ARCHIVE_DIR/source"
mkdir -p "$ARCHIVE_DIR/validators"

# Function to safely move files
safe_move() {
    if [ -f "$1" ]; then
        echo -e "  Moving: $1"
        mv "$1" "$ARCHIVE_DIR/$2"
    else
        echo -e "  ${YELLOW}Skip (not found): $1${NC}"
    fi
}

echo ""
echo -e "${YELLOW}Step 1: Archiving old/experimental versions...${NC}"
safe_move "generators/act1_generator_OLD.py" "generators/"
safe_move "generators/act1_generator_spec_driven.py" "generators/"
safe_move "source/act-1-who-we-are-GENERATED.md" "source/"
safe_move "source/act-1-who-we-are-SPEC-DRIVEN.md" "source/"
safe_move "test_document_builders.py" ""

echo ""
echo -e "${YELLOW}Step 2: Archiving development documentation...${NC}"
safe_move "ACT_3_4_5_DATA_MAPPING.md" ""
safe_move "DATA_ACCURACY_VERIFICATION.md" ""
safe_move "DATA_INVENTORY_REVISED.md" ""
safe_move "HALLUCINATION_REPORT.md" ""
safe_move "HOW-TO-BUILD-ACT-1.md" ""
safe_move "IMPLEMENTATION_SUMMARY_03_04.md" ""
safe_move "MODULAR-ARCHITECTURE-SUMMARY.md" ""
safe_move "RESEARCH_DATA_ASSESSMENT.md" ""
safe_move "STRATEGIC_FOUNDATION.md" ""
safe_move "generators/IMPLEMENTATION_SUMMARY_01_02.md" "generators/"
safe_move "generators/INTEGRATION_GUIDE_01_02.md" "generators/"
safe_move "generators/README_BUILDERS.md" "generators/"
safe_move "generators/README_BUILDERS_03_04.md" "generators/"

echo ""
echo -e "${YELLOW}Step 3: Archiving validator reports...${NC}"
if [ -d "validators/reports" ]; then
    echo -e "  Moving: validators/reports/"
    mv validators/reports "$ARCHIVE_DIR/validators/"
else
    echo -e "  ${YELLOW}Skip (not found): validators/reports/${NC}"
fi

echo ""
echo -e "${YELLOW}Step 4: Archiving potentially unused files...${NC}"
safe_move "verify_hallucinations.py" ""
safe_move "generators/spec_parser.py" "generators/"
safe_move "generators/template_renderer.py" "generators/"
safe_move "generators/act2_data_loader.py" "generators/"

echo ""
echo -e "${YELLOW}Step 5: Archiving this cleanup audit...${NC}"
safe_move "CLEANUP_AUDIT_2025-10-24.md" ""

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Cleanup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Count remaining files
REMAINING_FILES=$(find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.html" \) ! -path "./$ARCHIVE_DIR/*" ! -path "./docs/*" ! -path "./.git/*" | wc -l)

echo -e "Files archived to: ${GREEN}$ARCHIVE_DIR/${NC}"
echo -e "Remaining project files: ${GREEN}$REMAINING_FILES${NC}"
echo ""

echo -e "${YELLOW}Next steps:${NC}"
echo "1. Test the build: ${GREEN}python3 build.py${NC}"
echo "2. If everything works, you can remove the archive: ${RED}rm -rf $ARCHIVE_DIR${NC}"
echo "3. Or keep the archive for safety"
echo ""

# Create a simple README if it doesn't exist
if [ ! -f "README.md" ]; then
    echo -e "${YELLOW}Creating README.md...${NC}"
    cat > README.md << 'EOF'
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
EOF
    echo -e "${GREEN}README.md created!${NC}"
fi

echo ""
echo -e "${GREEN}Done! Your project is now clean and production-ready.${NC}"