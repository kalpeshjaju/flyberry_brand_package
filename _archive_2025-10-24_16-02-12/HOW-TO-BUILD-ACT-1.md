# HOW TO BUILD ACT 1: MODULAR ARCHITECTURE GUIDE

**Version**: 2.0
**Last Updated**: 2025-10-23
**Purpose**: Complete guide to the modular Act 1 build system

---

## 🎯 THE PROBLEM WE SOLVED

**Before**: Long comprehensive document (30,000 words) that was:
- ❌ Hard to update (change one standard → edit entire document)
- ❌ Hard to maintain consistency (easy to miss sections when updating)
- ❌ Difficult to version control (single massive file)
- ❌ Not modular (couldn't update structure independently from content)

**After**: Modular 3-layer architecture that is:
- ✅ Easy to update (change one file → rebuild → all docs updated)
- ✅ Maintains consistency (all docs follow same blueprint)
- ✅ Version control friendly (see exactly what changed)
- ✅ Fully modular (structure ≠ standards ≠ content)

---

## 📐 THE 3-LAYER ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│ LAYER 1: STANDARDS (What quality looks like)           │
│ File: act-1-master-blueprint.md                         │
│                                                          │
│ Defines:                                                 │
│ - Content frameworks (Pyramid, MECE, SO WHAT)          │
│ - Writing standards (tone, voice, formatting)          │
│ - Specificity rules (no generic claims)                │
│ - Quality rubric (5 dimensions, 100 points)            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ LAYER 2: STRUCTURE (How each document is organized)    │
│ Folder: act-1-document-specs/                          │
│                                                          │
│ Contains 7 files:                                        │
│ - doc-00-brand-foundation.md (10 sections) ✅         │
│ - doc-01-product-portfolio.md (8 sections) ✅         │
│ - doc-02-sourcing-philosophy.md (7 sections) ✅       │
│ - doc-03-hero-products.md (4 sections) ✅             │
│ - doc-04-nutritional-excellence.md (5 sections) ✅    │
│ - doc-05-fortune-500-validation.md (5 sections) ✅    │
│ - doc-06-brand-promise.md (5 sections) ✅             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ LAYER 3: CONTENT (Actual data)                         │
│ Files: *.json, brand-foundation.md                     │
│                                                          │
│ Contains:                                                │
│ - brand-foundation.md (mission, vision, positioning)   │
│ - products/*.json (13 products with details)           │
│ - design.json (colors, typography)                     │
│ - recipes/*.json (11 recipes)                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ GENERATOR: generators/act1_generator.py                │
│                                                          │
│ Process:                                                 │
│ 1. Read Layer 1 (understand standards)                 │
│ 2. Read Layer 2 (understand structure)                 │
│ 3. Pull Layer 3 (get data)                             │
│ 4. Apply standards to structure + data                 │
│ 5. Generate markdown → HTML                            │
└─────────────────────────────────────────────────────────┘
                          ↓
                  docs/act-1-who-we-are.html
```

---

## 📂 FILE LOCATIONS

### **INPUT Folder** (Source of Truth)
```
/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data/

├── act-1-master-blueprint.md           ← LAYER 1: Standards
├── act-1-document-specs/               ← LAYER 2: Structure
│   ├── README.md                       ← Architecture guide
│   ├── doc-00-brand-foundation.md      ← ✅ Complete
│   ├── doc-01-product-portfolio.md     ← TODO
│   ├── doc-02-sourcing-philosophy.md   ← TODO
│   ├── doc-03-hero-products.md         ← TODO
│   ├── doc-04-nutritional-excellence.md ← TODO
│   ├── doc-05-fortune-500-validation.md ← TODO
│   └── doc-06-brand-promise.md         ← TODO
├── brand-foundation.md                 ← LAYER 3: Brand data
├── products/                           ← LAYER 3: Product data
│   ├── medjoul-dates.json
│   ├── brazil-nuts.json
│   └── [11 more products]
├── recipes/                            ← LAYER 3: Recipe data
│   └── [11 recipes]
└── design.json                         ← LAYER 3: Design system
```

### **OUTPUT Folder** (Generated)
```
/Users/kalpeshjaju/Development/flyberry_brand_package/

├── generators/
│   └── act1_generator.py               ← Generator logic
├── source/
│   └── act-1-who-we-are.md             ← Generated markdown
└── docs/
    └── act-1-who-we-are.html           ← Final HTML
```

---

## 🔄 HOW TO MAKE CHANGES

### **Scenario 1: Change Writing Style**
**Example**: Make tone more conversational

**Steps**:
1. Edit: `act-1-master-blueprint.md` → Writing Standards section
2. Update tone guidelines (e.g., "use more contractions, shorter sentences")
3. Run: `python3 build.py`
4. Result: All 7 documents rebuilt with new tone

**Files Changed**: 1 (blueprint only)
**Propagation**: Automatic to all documents

---

### **Scenario 2: Add New Section to Document**
**Example**: Add "Our History" section to Document 00

**Steps**:
1. Edit: `act-1-document-specs/doc-00-brand-foundation.md`
2. Add new section template (Section 11: Our History)
3. Update generator: Add logic to pull history data
4. Run: `python3 build.py`
5. Result: Document 00 now has new section, others unchanged

**Files Changed**: 2 (doc spec + generator)
**Propagation**: Only affects Document 00

---

### **Scenario 3: Update Brand Positioning**
**Example**: Change tagline or mission statement

**Steps**:
1. Edit: `brand-foundation.md` → Update mission/tagline
2. Run: `python3 build.py`
3. Result: New mission/tagline appears wherever referenced (Doc 00, index, etc.)

**Files Changed**: 1 (data only)
**Propagation**: Automatic wherever mission/tagline is used

---

### **Scenario 4: Add New Product**
**Example**: Add Pistachio Nuts to catalog

**Steps**:
1. Create: `products/pistachio-nuts.json` with complete data
2. Run: `python3 build.py`
3. Result:
   - Document 00: Product count updates (13 → 14)
   - Document 01: New product appears in catalog
   - Document 02: Origin count updates if new country
   - Document 04: Nutritional data added if RDA > 20%

**Files Changed**: 1 (new product JSON)
**Propagation**: Automatic across all relevant documents

---

### **Scenario 5: Change Quality Standards**
**Example**: Require 99% confidence instead of 95%

**Steps**:
1. Edit: `act-1-master-blueprint.md` → Confidence Hierarchy section
2. Update confidence levels and requirements
3. Run: `python3 build.py`
4. Result: All documents now cite confidence with new standard

**Files Changed**: 1 (blueprint only)
**Propagation**: Automatic to all documents

---

## ✅ MODULAR BENEFITS

### **1. Easy Updates**
- Change one file → rebuild → all affected documents update
- No manual copy-paste across documents
- No risk of forgetting to update one document

### **2. Consistency Guaranteed**
- All documents follow same blueprint (standards)
- All documents use same data sources (JSON)
- All documents apply same quality rubric

### **3. Version Control Friendly**
- See exactly what changed in each file
- Rollback individual components (blueprint, spec, data)
- Track changes over time clearly

### **4. Maintainable at Scale**
- Add new documents: Create new spec
- Change standards: Update blueprint
- Update content: Edit JSON data
- Each layer independent

### **5. Understandable**
- Blueprint: WHY (principles, standards)
- Specs: WHAT (structure, sections)
- Data: CONTENT (actual information)
- Generator: HOW (processing logic)

---

## 🏗️ CURRENT STATUS

### **✅ Complete**:
- [x] Master blueprint created (act-1-master-blueprint.md)
- [x] Document 00 spec created (doc-00-brand-foundation.md)
- [x] **Document 01-06 specs created** (all 6 specs complete) ✨ NEW
- [x] README created (explains architecture)
- [x] Brand foundation data exists (brand-foundation.md)
- [x] Product data exists (13 products JSON)
- [x] Generator updated to use brand-foundation.md
- [x] Build pipeline working (JSON → Markdown → HTML)

### **⏳ TODO (Phase 2)**:
- [ ] Update generator to read document specs dynamically (not hardcode structure)
- [ ] Implement spec-driven content generation
- [ ] Test modular updates (change spec → rebuild → verify propagation)
- [ ] Create generators for Acts 2-5 using same architecture

---

## 📋 QUICK REFERENCE

### **What Lives Where**

| What | Where | When to Update |
|------|-------|----------------|
| Overall standards | `act-1-master-blueprint.md` | Writing style, quality rubric, content frameworks change |
| Document structure | `act-1-document-specs/doc-XX-*.md` | Section order, templates, requirements change |
| Brand positioning | `brand-foundation.md` | Mission, vision, tagline, strategy change |
| Product details | `products/*.json` | New products, spec changes, price updates |
| Design system | `design.json` | Colors, typography, packaging changes |
| Generator logic | `generators/act1_generator.py` | Processing rules, data sources, output format change |

### **Common Commands**

```bash
# Rebuild entire Act 1
python3 build.py

# Rebuild just Act 1 (if multiple acts exist)
python3 build.py act-1-who-we-are

# View generated markdown (before HTML conversion)
cat source/act-1-who-we-are.md

# View final HTML
open docs/act-1-who-we-are.html

# Check data integration
python3 data_integration.py

# Test Act 1 generator standalone
python3 generators/act1_generator.py
```

---

## 🎓 LEARNING THE SYSTEM

### **New Team Member Onboarding**

**Step 1: Understand the Layers**
1. Read: `act-1-master-blueprint.md` (10 min) - Learn standards
2. Read: `act-1-document-specs/README.md` (5 min) - Learn structure
3. Read: `brand-foundation.md` (5 min) - Learn brand positioning

**Step 2: Make a Small Change**
1. Edit: `brand-foundation.md` - Change one word in mission
2. Run: `python3 build.py`
3. View: `docs/act-1-who-we-are.html` - See change propagated

**Step 3: Make a Bigger Change**
1. Edit: `products/medjoul-dates.json` - Change price
2. Run: `python3 build.py`
3. View: Verify price updated in Document 01

**Step 4: Understand Quality**
1. Read: `act-1-master-blueprint.md` → Quality Checklist
2. Read: `act-1-master-blueprint.md` → Depth Score Rubric
3. Review: Generated HTML against rubric

**Total Time**: ~30 minutes to understand system, make changes, see results

---

## 🚀 NEXT STEPS

### **Phase 1: Complete Act 1 Modular System** (Current)
- [ ] Create remaining 6 document specs (docs 01-06)
- [ ] Update generator to read specs (not hardcode structure)
- [ ] Test full modular workflow
- [ ] Document edge cases

### **Phase 2: Extend to Acts 2-5**
- [ ] Create act-2-master-blueprint.md
- [ ] Create act-2-document-specs/ folder
- [ ] Build generators/act2_generator.py
- [ ] Repeat for Acts 3, 4, 5

### **Phase 3: Build System Automation**
- [ ] Add validation (check blueprint compliance)
- [ ] Add testing (verify data → HTML pipeline)
- [ ] Add CI/CD (auto-rebuild on data changes)

---

## 💡 KEY INSIGHTS

### **Why This Architecture Works**

**1. Separation of Concerns**:
- Standards ≠ Structure ≠ Content
- Change one without affecting others
- Each layer has single responsibility

**2. Single Source of Truth**:
- Blueprint defines standards (one place)
- Data defines content (JSON files)
- No duplication, no inconsistency

**3. Automated Consistency**:
- Generator enforces standards automatically
- Can't build doc that violates blueprint
- Quality baked into process

**4. Future-Proof**:
- Add new standards → rebuild → all docs comply
- Add new documents → create spec → generator includes
- Change data → rebuild → all references update

---

## 📞 SUPPORT

**Questions?**
- Check: `act-1-document-specs/README.md` (FAQ section)
- Check: This file (HOW-TO-BUILD-ACT-1.md)
- Check: `act-1-master-blueprint.md` (comprehensive guide)

**Common Issues**:
1. **Build fails**: Check data_integration.py loaded correctly
2. **Output wrong**: Check data source file paths
3. **Inconsistent quality**: Check generator follows blueprint
4. **Missing content**: Check JSON data complete

---

**Last Updated**: 2025-10-23
**Version**: 2.1 - All Document Specs Complete
**Status**: Phase 1 complete (All 7 doc specs created ✅), Phase 2 next (spec-driven generator)
