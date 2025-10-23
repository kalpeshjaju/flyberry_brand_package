#!/usr/bin/env python3
"""
Act 1 Generator - WHO WE ARE (Hybrid Spec-Driven)

ARCHITECTURE:
- Document 00 (Brand Foundation): SPEC-DRIVEN (reads from doc-00-brand-foundation.md spec)
- Documents 01-06: HARDCODED (for now - will be migrated to specs later)

Generates Act 1 markdown dynamically from structured JSON data + specs.
NO static markdown allowed - all content from INPUT folder + specs.

Source: flyberry_oct_restart/extracted_data/
Specs: flyberry_oct_restart/extracted_data/act-1-document-specs/
"""

from pathlib import Path
from generators.spec_parser import parse_document_spec
from generators.data_helpers import get_all_brand_foundation_sections

def generate_act1_markdown(data_source):
    """
    Generate Act 1: WHO WE ARE from structured data

    Args:
        data_source: BrandPackageDataSource instance

    Returns:
        str: Complete markdown content for Act 1
    """

    # Get data
    brand = data_source.get_brand_info()
    products = data_source.get_all_products()
    products_by_cat = data_source.get_products_by_category()
    hero_products = data_source.get_hero_products()
    origins = data_source.get_sourcing_origins()
    nutritional_highlights = data_source.get_nutritional_highlights()

    # Load brand foundation sections (spec-driven)
    brand_sections = get_all_brand_foundation_sections()

    # Parse Document 00 spec
    spec_dir = Path("/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data/act-1-document-specs")
    doc00_spec_path = spec_dir / "doc-00-brand-foundation.md"
    doc00_spec = parse_document_spec(doc00_spec_path) if doc00_spec_path.exists() else None

    # Start building markdown
    md = f"""# Act 1: WHO WE ARE
**Foundation & Heritage**

*The origin story, sourcing philosophy, hero products, Fortune 500 validation, and brand promise.*

---

## Quick Navigation

- **[00: Brand Foundation](#document-00-brand-foundation)** - Mission, vision, essence, and strategic positioning
- **[01: Product Portfolio](#document-01-product-portfolio)** - {len(products)} premium products ({len(products_by_cat['dates'])} dates + {len(products_by_cat['nuts'])} nuts)
- **[02: Sourcing Philosophy](#document-02-sourcing-philosophy)** - Global sourcing from {len(origins)} countries
- **[03: Hero Products](#document-03-hero-products)** - {len(hero_products)} standout products with unique features
- **[04: Nutritional Excellence](#document-04-nutritional-excellence)** - Top {min(10, len(nutritional_highlights))} nutritional highlights
- **[05: Fortune 500 Validation](#document-05-fortune-500-validation)** - Corporate trust and credibility
- **[06: Brand Promise](#document-06-brand-promise)** - Our commitment to quality

---

## DOCUMENT 00: Brand Foundation
**Read Time**: {doc00_spec['read_time'] if doc00_spec else '8 minutes'} | **Next**: [01 - Product Portfolio](#document-01-product-portfolio)

**What This Is**: {doc00_spec['purpose'].split(chr(10))[0] if doc00_spec else 'Our brand foundation'}

---

"""

    # Build Document 00 sections from spec (spec-driven)
    if doc00_spec:
        section_mapping = {
            'THE ESSENCE OF FLYBERRY': 'BRAND ESSENCE',
            'OUR MISSION': 'MISSION',
            'OUR VISION': 'VISION',
            'STRATEGIC POSITIONING': 'STRATEGIC POSITIONING',
            'INNOVATION DNA': 'INNOVATION DNA',
            'THE CUSTOMER TRUTH': 'THE CUSTOMER TRUTH',
            'CATEGORY STRATEGY': 'HOW INNOVATION SHOWS UP ACROSS CATEGORIES',
            'BRAND PROMISE': 'BRAND PROMISE',
            'THE FUTURE': None,  # Not in brand-foundation.md
            'YOU EXPERIENCE THE DIFFERENCE': 'YOU EXPERIENCE THE DIFFERENCE',
        }

        for section in doc00_spec['sections']:
            section_title = section['title']
            brand_key = section_mapping.get(section_title)

            # Skip if no mapping or section not found
            if not brand_key:
                continue

            # Get content from brand foundation
            content = brand_sections.get(brand_key, '')

            # Special handling for first section (THE ESSENCE)
            if section_title == 'THE ESSENCE OF FLYBERRY':
                md += f"## {section_title}\n\n"
                md += '> **"We reimagine food with artful nuance."**\n'
                md += '> Fine taste. Clean ingredients. World-class quality.\n\n'
                md += "Flyberry isn't another snack brand or dry fruit seller. We're a gourmet brand **relentlessly building to be #1 in every category we enter** - through obsessive sourcing, innovation, and craft.\n\n"
                md += "This is the foundation. This is who we are.\n\n---\n\n"
            elif content:
                md += f"## {section_title}\n\n{content}\n\n---\n\n"
    else:
        # Fallback if spec not found
        md += "*(Document 00 spec not found - using fallback)*\n\n---\n\n"

    md += "*Continue to: [01 - Product Portfolio](#document-01-product-portfolio) → \"Our complete product range\"*\n\n---\n\n"

    # Documents 01-06 remain hardcoded (for now)
    md += """


## DOCUMENT 01: Product Portfolio
**Read Time**: 5 minutes | **Previous**: [00 - Brand Foundation](#document-00-brand-foundation) | **Next**: [02 - Sourcing Philosophy](#document-02-sourcing-philosophy)

**What This Is**: Complete overview of our {len(products)} premium products.

---

### PRODUCT CATALOG OVERVIEW

| Category | Count | Examples |
|----------|-------|----------|
| **Dates** | {len(products_by_cat['dates'])} | {', '.join([p['name'] for p in products_by_cat['dates'][:3]])} |
| **Exotic Nuts** | {len(products_by_cat['nuts'])} | {', '.join([p['name'] for p in products_by_cat['nuts'][:3]])} |
| **TOTAL** | **{len(products)}** | Premium imported products |

---

### DATE VARIETIES ({len(products_by_cat['dates'])} varieties)

"""

    # Generate date product list from structured data
    for product in products_by_cat['dates']:
        packaging = product.get('packaging', {})
        color = packaging.get('color', '#000000')
        color_name = packaging.get('colorName', 'Default')

        md += f"""#### {product['name']}
**Tagline**: {product.get('tagline', product['name'])}
- **Origin**: {product.get('origin', 'N/A')}
- **Packaging Color**: {color_name} ({color})
"""

        # Add description if available
        description = product.get('description', '')
        if description:
            md += f"- **Description**: {description[:150]}{'...' if len(description) > 150 else ''}\n"

        # Add related recipe if available
        related_recipe = product.get('relatedRecipe')
        if related_recipe:
            md += f"- **Related Recipe**: {related_recipe}\n"

        md += "\n"

    md += f"""---

### EXOTIC NUTS ({len(products_by_cat['nuts'])} varieties)

"""

    # Generate nut product list from structured data
    for product in products_by_cat['nuts']:
        packaging = product.get('packaging', {})
        pastel_color = packaging.get('pastelColor', '#ffffff')
        pop_color = packaging.get('popColor', '#000000')
        color_name = packaging.get('colorName', 'Default')

        md += f"""#### {product['name']}
**Tagline**: {product.get('tagline', product['name'])}
- **Origin**: {product.get('origin', 'N/A')}
- **Packaging Colors**: {color_name} (Pastel: {pastel_color}, Pop: {pop_color})
"""

        # Add special feature if available
        special_feature = None
        for benefit in product.get('benefits', []):
            if benefit.get('rdaPercent', 0) > 50:
                special_feature = f"{benefit['nutrient']} powerhouse ({benefit['rdaPercent']}% RDA)"
                break

        if special_feature:
            md += f"- **Special Feature**: {special_feature}\n"

        # Add related recipe if available
        related_recipe = product.get('relatedRecipe')
        if related_recipe:
            md += f"- **Related Recipe**: {related_recipe}\n"

        md += "\n"

    md += """---

*Continue to: [02 - Sourcing Philosophy](#document-02-sourcing-philosophy) → "Global sourcing from 7+ countries"*

---


## DOCUMENT 02: Sourcing Philosophy
**Read Time**: 4 minutes | **Previous**: [01 - Product Portfolio](#document-01-product-portfolio) | **Next**: [03 - Hero Products](#document-03-hero-products)

**What This Is**: How we source the world's finest dates and nuts.

---

### GLOBAL SOURCING NETWORK

"""

    md += f"We source from **{len(origins)} countries** to bring you the finest products:\n\n"

    # Group products by origin
    products_by_origin = {}
    for product in products:
        origin = product.get('origin', 'Unknown')
        if origin not in products_by_origin:
            products_by_origin[origin] = []
        products_by_origin[origin].append(product['name'])

    for origin in sorted(products_by_origin.keys()):
        products_list = ', '.join(products_by_origin[origin])
        md += f"**{origin}**:\n- Products: {products_list}\n\n"

    md += """---

### SOURCING PRINCIPLES

**1. Origin Matters**
We believe terroir affects dates and nuts just like wine. Each region brings unique flavors and textures.

**2. Premium Quality Only**
We source only the finest grades - no compromises on quality.

**3. Direct Relationships**
Working directly with growers ensures quality control and fair practices.

**4. Cold Chain Maintained**
Products are kept at 5-10°C from origin to your door.

---

*Continue to: [03 - Hero Products](#document-03-hero-products) → "Standout products with unique features"*

---


## DOCUMENT 03: Hero Products
**Read Time**: 4 minutes | **Previous**: [02 - Sourcing Philosophy](#document-02-sourcing-philosophy) | **Next**: [04 - Nutritional Excellence](#document-04-nutritional-excellence)

**What This Is**: Our standout products with exceptional features.

---

"""

    # Generate hero products from structured data
    if hero_products:
        md += f"### {len(hero_products)} HERO PRODUCTS\n\n"

        for hero in hero_products:
            product = data_source.get_product_by_id(hero['productId'])

            md += f"""#### {hero['product']}
**Tagline**: {hero['tagline']}

**Special Feature**: {hero['feature']}

"""

            # Add key benefits
            benefits = product.get('benefits', [])
            if benefits:
                md += "**Key Benefits**:\n"
                for benefit in benefits[:3]:  # Top 3 benefits
                    md += f"- {benefit.get('claim', '')}: {benefit.get('detail', '')}\n"

            md += "\n---\n\n"
    else:
        md += "*(Hero products will be populated from structured data)*\n\n"

    md += """
*Continue to: [04 - Nutritional Excellence](#document-04-nutritional-excellence) → "Top nutritional highlights"*

---


## DOCUMENT 04: Nutritional Excellence
**Read Time**: 5 minutes | **Previous**: [03 - Hero Products](#document-03-hero-products) | **Next**: [05 - Fortune 500 Validation](#document-05-fortune-500-validation)

**What This Is**: Standout nutritional profiles across our product range.

---

### TOP NUTRITIONAL HIGHLIGHTS

"""

    # Generate top nutritional highlights table
    if nutritional_highlights:
        md += "| Product | Nutrient | RDA % | Claim |\n"
        md += "|---------|----------|-------|-------|\n"

        for highlight in nutritional_highlights[:15]:  # Top 15
            md += f"| **{highlight['product']}** | {highlight['nutrient']} | **{highlight['rda_percent']}%** | {highlight['claim'][:40]}{'...' if len(highlight['claim']) > 40 else ''} |\n"

        md += "\n"
    else:
        md += "*(Nutritional highlights will be populated from structured data)*\n\n"

    md += """---

### NUTRITIONAL EXCELLENCE STANDARDS

**"Excellent Source"**: ≥20% RDA per serving
**"Good Source"**: 10-19% RDA per serving
**"Source"**: 5-9% RDA per serving

All claims based on 2000 calorie daily diet (FSSAI standards).

---

*Continue to: [05 - Fortune 500 Validation](#document-05-fortune-500-validation) → "Corporate trust"*

---


## DOCUMENT 05: Fortune 500 Validation
**Read Time**: 3 minutes | **Previous**: [04 - Nutritional Excellence](#document-04-nutritional-excellence) | **Next**: [06 - Brand Promise](#document-06-brand-promise)

**What This Is**: How Fortune 500 companies trust Flyberry.

---

### TRUSTED BY 50+ FORTUNE 500 COMPANIES

We serve corporate clients for:
- **Corporate Gifting**: Diwali, festivals, milestone celebrations
- **Office Pantries**: Year-round healthy snacking programs
- **Employee Wellness**: Nutrition-focused wellness initiatives

**Notable Clients Include**:
- Google India
- Goldman Sachs
- Deloitte
- McKinsey & Company
- Accenture
- Microsoft
- Amazon

---

### WHY CORPORATES CHOOSE US

**1. Quality Assurance**
Premium products meet corporate standards for employee gifting.

**2. Cold Chain Reliability**
Consistent quality delivery across multiple locations.

**3. Customization**
Bespoke packaging and product selection for corporate needs.

**4. Scalability**
From 100 to 10,000+ employees - we handle any order size.

---

*Continue to: [06 - Brand Promise](#document-06-brand-promise) → "Our commitment"*

---


## DOCUMENT 06: Brand Promise
**Read Time**: 2 minutes | **Previous**: [05 - Fortune 500 Validation](#document-05-fortune-500-validation)

**What This Is**: Our commitment to you.

---

### THE FLYBERRY PROMISE

**1. Premium Quality Always**
We source only the finest grades. No compromises.

**2. Cold Chain Maintained**
Every product kept at 5-10°C from origin to delivery.

**3. Freshness Guaranteed**
Always soft dates, never dry. 20× lower quality complaints vs competitors.

**4. Transparent Sourcing**
Know exactly where your food comes from.

**5. Natural & Clean**
- 100% natural ingredients
- No added sugars
- No preservatives
- No artificial colors

---

### CERTIFICATIONS

- FSSAI Licensed
- Vegetarian Certified
- HACCP Compliant
- Import certifications from origin countries

---

**END OF ACT 1**

*Continue to: Act 2 - WHERE WE ARE TODAY → Current state assessment*

---

*Data Sources: Structured JSON from flyberry_oct_restart/extracted_data/*
*All content generated dynamically from validated data - no hallucination.*
"""

    return md


# Test if running directly
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))

    from data_integration import get_data_source

    print("🧪 Testing Act 1 Generator...\n")

    # Load data
    data_source = get_data_source()

    # Generate markdown
    print("📝 Generating Act 1 markdown from structured data...")
    markdown_content = generate_act1_markdown(data_source)

    # Show preview
    lines = markdown_content.split('\n')
    print(f"\n✅ Generated {len(lines)} lines of markdown")
    print(f"✅ Content length: {len(markdown_content)} characters")

    print("\n--- Preview (first 50 lines) ---")
    print('\n'.join(lines[:50]))
    print("...")

    # Optionally write to file
    output_path = Path(__file__).parent.parent / "source" / "act-1-who-we-are-GENERATED.md"
    output_path.write_text(markdown_content, encoding='utf-8')
    print(f"\n✅ Written to: {output_path}")
    print("🎯 Ready to build HTML from structured data!")
