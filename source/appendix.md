# APPENDIX
**Supporting Documentation**

Additional resources: data lineage, claims registry, product catalog references, design assets, and validation reports.

---

## Quick Navigation

- **[00: Data Sources & Lineage](#document-00-data-sources--lineage)** – Where each claim/data point comes from
- **[01: Claims Registry](#document-01-claims-registry)** – Health, nutritional, and product claims tracking
- **[02: Product Catalog Summary](#document-02-product-catalog-summary)** – Master list and identifiers
- **[03: Design System & Assets](#document-03-design-system--assets)** – CSS, components, and brand usage
- **[04: Test & Validation Reports](#document-04-test--validation-reports)** – Build, content, and product validation
- **[05: Technical Stack Summary](#document-05-technical-stack-summary)** – Project structure and tech overview

---

## DOCUMENT 00: Data Sources & Lineage
**What This Is**: Overview of structured inputs and how data flows into generated outputs.

### PIPELINE OVERVIEW

```
raw_data/ → llm_readable/ → extracted_data/ → generators/ → HTML output
```

### KEY REFERENCES

- System analysis: `FLYBERRY_OCT_RESTART_ANALYSIS_2025-10-24.md`
- Reference system: `REFERENCE_DATA_SYSTEM.md`
- Research tasks: `RESEARCH_NEEDED.md`

---

## DOCUMENT 01: Claims Registry
**Purpose**: Track claims, their sources, and verification status.

- Health/nutritional claims: maintained under the data source repository
- Verification: marked with confidence and source linkage
- Anti‑hallucination validator: `generators/anti_hallucination_validator.py`

---

## DOCUMENT 02: Product Catalog Summary
**Purpose**: At‑a‑glance summary of products listed in Act 1.

- 13 products (8 date varieties + 5 exotic nuts)
- Names, origins, and taglines are rendered in Act 1 from structured data

---

## DOCUMENT 03: Design System & Assets
**Purpose**: Where to find CSS, components, and any custom styling per page.

- Global styles: `assets/css/styles.css`
- Per‑page custom CSS (if present): `assets/css/<page>-custom.css`
- Template used: `templates/act.html`

---

## DOCUMENT 04: Test & Validation Reports
**Purpose**: Consolidated pointers to quality checks and outcomes.

- Product Validation Report: `PRODUCT_VALIDATION_REPORT_2025-10-24.md`
- Product Test Report (JSON): `PRODUCT_TEST_REPORT.json`
- Final Test Summary: `FINAL_TEST_REPORT_2025-10-24.md`

---

## DOCUMENT 05: Technical Stack Summary
**Purpose**: Quick reference for developers/operators.

- Entry point: `build.py`
- Generators: `generators/act1_generator.py`, `generators/act2_generator.py`
- Data source connector: `data_integration.py`
- Output: `docs/`

> Note: Acts 3–5 are currently authored as Markdown in `source/` and will be migrated to structured data generation.

