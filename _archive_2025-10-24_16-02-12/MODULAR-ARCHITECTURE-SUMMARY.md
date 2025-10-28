# ACT 1 MODULAR ARCHITECTURE - VISUAL SUMMARY

**Quick Reference**: How the modular system works at a glance

---

## 🎯 THE CORE CONCEPT

**ONE INPUT DOC** (act-1-master-blueprint.md) **+** **MODULAR SPECS** (7 document templates) **→** **CONSISTENT OUTPUT** (HTML)

Change input → Rebuild → Output updates automatically across all 7 documents.

---

## 📐 THE 3-LAYER STACK

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: STANDARDS (The Rules)                            │
│  📄 act-1-master-blueprint.md                               │
│                                                              │
│  ▸ Content Frameworks: Pyramid, MECE, SO WHAT, Confidence │
│  ▸ Writing Standards: Tone, Voice, Formatting, Rhythm     │
│  ▸ Specificity Rules: 254.5% (not "high in")              │
│  ▸ Quality Rubric: 5 dimensions, 100 points               │
│                                                              │
│  Updates here → Apply to ALL 7 documents                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: STRUCTURE (The Templates)                        │
│  📁 act-1-document-specs/                                   │
│                                                              │
│  ▸ doc-00-brand-foundation.md (10 sections) ✅             │
│  ▸ doc-01-product-portfolio.md (8 sections) TODO          │
│  ▸ doc-02-sourcing-philosophy.md (7 sections) TODO        │
│  ▸ doc-03-hero-products.md (4 sections) TODO              │
│  ▸ doc-04-nutritional-excellence.md (5 sections) TODO     │
│  ▸ doc-05-fortune-500-validation.md (6 sections) TODO     │
│  ▸ doc-06-brand-promise.md (7 sections) TODO              │
│                                                              │
│  Updates here → Apply to THAT document only                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: CONTENT (The Data)                               │
│  📄 *.json, brand-foundation.md                             │
│                                                              │
│  ▸ brand-foundation.md (mission, vision, positioning)     │
│  ▸ products/*.json (13 products × 7 attributes each)      │
│  ▸ design.json (colors, typography, packaging)            │
│  ▸ recipes/*.json (11 recipes)                            │
│                                                              │
│  Updates here → Propagate wherever data is used            │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ⚙️ GENERATOR COMBINES
                              ↓
                    📄 act-1-who-we-are.html
```

---

## 🔄 UPDATE WORKFLOWS

### **Scenario A: Change Standards** (Affects ALL documents)
```
Edit: act-1-master-blueprint.md
   ↓
Example: "Make tone more conversational"
   ↓
Rebuild: python3 build.py
   ↓
Result: All 7 documents now conversational
```

**Effort**: 5 minutes
**Impact**: 7 documents

---

### **Scenario B: Change Structure** (Affects ONE document)
```
Edit: doc-00-brand-foundation.md
   ↓
Example: "Add 'Our History' section"
   ↓
Rebuild: python3 build.py
   ↓
Result: Only Doc 00 has new section
```

**Effort**: 10 minutes
**Impact**: 1 document

---

### **Scenario C: Change Content** (Affects WHERE USED)
```
Edit: brand-foundation.md
   ↓
Example: "Change mission statement"
   ↓
Rebuild: python3 build.py
   ↓
Result: New mission appears in Doc 00, index, anywhere else it's referenced
```

**Effort**: 2 minutes
**Impact**: Wherever mission is used

---

## 📊 WHAT'S MODULAR

| Component | File | Scope | Update Frequency |
|-----------|------|-------|------------------|
| **Standards** | act-1-master-blueprint.md | All documents | Quarterly (when standards evolve) |
| **Structure (Doc 00)** | doc-00-brand-foundation.md | Doc 00 only | Monthly (when section needs change) |
| **Structure (Doc 01)** | doc-01-product-portfolio.md | Doc 01 only | Monthly |
| **Structure (Doc 02)** | doc-02-sourcing-philosophy.md | Doc 02 only | Monthly |
| **Structure (Doc 03)** | doc-03-hero-products.md | Doc 03 only | Monthly |
| **Structure (Doc 04)** | doc-04-nutritional-excellence.md | Doc 04 only | Monthly |
| **Structure (Doc 05)** | doc-05-fortune-500-validation.md | Doc 05 only | Monthly |
| **Structure (Doc 06)** | doc-06-brand-promise.md | Doc 06 only | Monthly |
| **Brand Positioning** | brand-foundation.md | Where used | Quarterly (strategic pivots) |
| **Product Data** | products/*.json | Where used | Weekly (new products, updates) |
| **Design System** | design.json | Where used | Monthly (design updates) |

---

## ✅ BENEFITS AT A GLANCE

| Benefit | Old Way | New Way |
|---------|---------|---------|
| **Update standards** | Edit 7 places manually | Edit 1 file, rebuild |
| **Add new section** | Copy-paste template 7 times | Edit 1 doc spec |
| **Change product price** | Find all references, update each | Edit 1 JSON, rebuild |
| **Ensure consistency** | Manual review, easy to miss | Automatic enforcement |
| **Version control** | Big files, unclear what changed | Small files, clear changes |
| **Onboarding** | Read 30k word doc | Read 3 short files (10 min) |

---

## 🎯 QUICK START

### **1. Understand (5 minutes)**
```bash
# Read the blueprint (understand standards)
cat flyberry_oct_restart/extracted_data/act-1-master-blueprint.md

# Read one doc spec (understand structure)
cat flyberry_oct_restart/extracted_data/act-1-document-specs/doc-00-brand-foundation.md

# Read brand data (understand content)
cat flyberry_oct_restart/extracted_data/brand-foundation.md
```

### **2. Make a Change (2 minutes)**
```bash
# Edit brand foundation (change one word in mission)
vim flyberry_oct_restart/extracted_data/brand-foundation.md

# Rebuild
python3 build.py
```

### **3. Verify (1 minute)**
```bash
# Open HTML and verify change propagated
open docs/act-1-who-we-are.html
```

**Total Time**: 8 minutes to understand + change + verify

---

## 📁 FILE TREE

```
flyberry_oct_restart/extracted_data/        (INPUT - Source of Truth)
├── act-1-master-blueprint.md               ← Standards for all docs
├── act-1-document-specs/                   ← Structure per doc
│   ├── README.md
│   ├── doc-00-brand-foundation.md          ← 10 section templates
│   ├── doc-01-product-portfolio.md         ← TODO
│   ├── doc-02-sourcing-philosophy.md       ← TODO
│   ├── doc-03-hero-products.md             ← TODO
│   ├── doc-04-nutritional-excellence.md    ← TODO
│   ├── doc-05-fortune-500-validation.md    ← TODO
│   └── doc-06-brand-promise.md             ← TODO
├── brand-foundation.md                     ← Brand positioning data
├── products/                               ← Product data
│   ├── medjoul-dates.json
│   ├── brazil-nuts.json
│   └── [11 more]
└── design.json                             ← Design system data

flyberry_brand_package/                     (OUTPUT - Generated)
├── generators/
│   └── act1_generator.py                   ← Reads input → writes markdown
├── source/
│   └── act-1-who-we-are.md                 ← Generated markdown
└── docs/
    └── act-1-who-we-are.html               ← Final HTML
```

---

## 🚦 CURRENT STATUS

### **✅ DONE**
- [x] Master blueprint created (standards layer)
- [x] Doc 00 spec created (structure layer)
- [x] Brand data exists (content layer)
- [x] Generator updated (uses brand-foundation.md)
- [x] Build pipeline works (JSON → MD → HTML)
- [x] Architecture documented (3 guides created)

### **⏳ IN PROGRESS**
- [ ] Create specs for docs 01-06 (6 files)
- [ ] Update generator to read specs (not hardcode)
- [ ] Test modular updates (change → rebuild → verify)

### **📋 NEXT**
- [ ] Extend to Acts 2-5 (same architecture)
- [ ] Add validation (blueprint compliance)
- [ ] Add testing (data → HTML integrity)

---

## 🔑 KEY FILES

| File | Purpose | Update When |
|------|---------|-------------|
| `HOW-TO-BUILD-ACT-1.md` | **Read This First** - Complete guide to modular system | You need to understand system |
| `act-1-master-blueprint.md` | **Standards** - Quality rubric, frameworks, writing standards | Standards change |
| `act-1-document-specs/README.md` | **Architecture** - How layers work together | You need architecture overview |
| `doc-00-brand-foundation.md` | **Example** - Shows template structure | Creating new doc spec |
| `brand-foundation.md` | **Content** - Brand positioning data | Mission/vision/strategy changes |

---

## 💡 REMEMBER

**The Golden Rule**:
- **Don't edit HTML directly** (will be overwritten on rebuild)
- **Edit specs/data** (blueprint, doc specs, JSON files)
- **Rebuild** (python3 build.py)
- **Verify** (open HTML)

**The Modular Promise**:
- Change once → Propagates everywhere automatically
- Consistency guaranteed → Generator enforces standards
- Easy maintenance → Small files, clear responsibility
- Future-proof → Add new without breaking old

---

## 📞 HELP

**Start Here**: `HOW-TO-BUILD-ACT-1.md` (comprehensive guide)

**Quick Questions**:
- Where to change X? See "QUICK REFERENCE" section in HOW-TO-BUILD-ACT-1.md
- How to add Y? See "Scenario" sections in HOW-TO-BUILD-ACT-1.md
- Why isn't Z working? See "Common Issues" in HOW-TO-BUILD-ACT-1.md

---

**Last Updated**: 2025-10-23
**Version**: 2.0 - Modular Architecture
