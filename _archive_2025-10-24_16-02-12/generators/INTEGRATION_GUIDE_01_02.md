# Integration Guide: Document Builders 01 & 02

## Summary

Created spec-driven builders for Documents 01 (Product Portfolio) and 02 (Sourcing Philosophy) to replace hardcoded markdown in `act1_generator.py`.

## Files Created

- **`document_builders_01_02.py`** - Contains two builder functions:
  - `build_document_01(data_source)` - Product Portfolio
  - `build_document_02(data_source)` - Sourcing Philosophy

## How to Integrate into act1_generator.py

### Step 1: Import the builders

```python
# At the top of act1_generator.py
from generators.document_builders_01_02 import build_document_01, build_document_02
```

### Step 2: Replace hardcoded sections

**Current code (lines 114-252):**
```python
md += """

## DOCUMENT 01: Product Portfolio
**Read Time**: 5 minutes | **Previous**: [00 - Brand Foundation](#document-00-brand-foundation) | **Next**: [02 - Sourcing Philosophy](#document-02-sourcing-philosophy)

**What This Is**: Complete overview of our {len(products)} premium products.
...
[lots of hardcoded markdown]
...
"""
```

**New code:**
```python
# Document 01: Product Portfolio (spec-driven)
md += build_document_01(data_source)

# Document 02: Sourcing Philosophy (spec-driven)
md += build_document_02(data_source)
```

### Step 3: Remove hardcoded sections

Delete lines 114-252 in `act1_generator.py` and replace with the two function calls above.

## Verification

The builders have been tested and verified to:
- ✅ Generate identical structure to hardcoded version
- ✅ Use all data from structured JSON (no hardcoded content)
- ✅ Handle missing fields gracefully with defaults
- ✅ Match spec files exactly

## Testing

Run the test suite:
```bash
python3 generators/document_builders_01_02.py
```

Expected output:
```
🧪 Testing Document Builders 01 & 02...
📦 Loading structured data from INPUT folder...
✅ Loaded 13 products
📄 Building Document 01: Product Portfolio...
✅ Generated 4528 characters
📄 Building Document 02: Sourcing Philosophy...
✅ Generated 1630 characters
✅ All builders working correctly!
🎯 Ready to integrate into act1_generator.py
```

## Migration Progress

- [x] Document 00 (Brand Foundation) - SPEC-DRIVEN ✅
- [x] Document 01 (Product Portfolio) - SPEC-DRIVEN ✅
- [x] Document 02 (Sourcing Philosophy) - SPEC-DRIVEN ✅
- [ ] Document 03 (Hero Products) - HARDCODED ⏳
- [ ] Document 04 (Nutritional Excellence) - HARDCODED ⏳
- [ ] Document 05 (Quality Certifications) - HARDCODED ⏳
- [ ] Document 06 (Fortune 500 Validation) - HARDCODED ⏳

## Next Steps

1. Integrate these builders into `act1_generator.py`
2. Run full generation test to ensure output matches
3. Create builders for Documents 03-06
4. Complete Act 1 spec-driven migration
