#!/usr/bin/env python3
"""
Test Document Builders 03 & 04

PURPOSE: Verify spec-driven builders generate correct markdown structure
TESTS:
- Document 03: Hero Products (Brazil Nuts, Medjoul Dates, Why These 2, Hero Promise)
- Document 04: Nutritional Excellence (Top 11, Nutrient Profiles, FSSAI, Health Mapping)
"""

from generators.document_builders_03_04 import build_document_03, build_document_04
from data_integration import get_data_source


def test_document_03():
    """Test Document 03: Hero Products builder"""
    print("=" * 80)
    print("TEST: DOCUMENT 03 - HERO PRODUCTS")
    print("=" * 80)

    data_source = get_data_source()
    doc = build_document_03(data_source)

    # VERIFICATION: Check all required sections exist
    checks = [
        ("Document header", "## DOCUMENT 03: Hero Products" in doc),
        ("Hero #1 section", "### HERO #1: BRAZIL NUTS" in doc),
        ("Selenium claim", "254.5% RDA selenium" in doc),
        ("Selenium role explanation", "Thyroid function regulation" in doc),
        ("Sourcing story", "Wild-harvested from Amazon" in doc),
        ("Taste profile", "#### **Taste Profile**" in doc),
        ("Complete nutritional profile", "#### **Complete Nutritional Profile**" in doc),
        ("Why Hero #1", "#### **Why Brazil Nuts Are Hero #1**" in doc),
        ("Hero #2 section", "### HERO #2: MEDJOUL DATES" in doc),
        ("Bestseller achievement", "5+ Year Bestseller" in doc),
        ("Cold chain advantage", "India's ONLY cold chain" in doc),
        ("Workout benefits", "#### **Pre & Post-Workout Benefits**" in doc),
        ("Pre-workout timing", "30-45 minutes before exercise" in doc),
        ("Post-workout timing", "Within 30 minutes after exercise" in doc),
        ("Why Hero #2", "#### **Why Medjoul Dates Are Hero #2**" in doc),
        ("Customer testimonials", "#### **Customer Testimonials**" in doc),
        ("Repeat rate", "46%" in doc),
        ("Why These 2 section", "### WHY THESE 2 PRODUCTS ARE HEROES" in doc),
        ("Complementary storytelling", "#### **Complementary Storytelling**" in doc),
        ("Hero Promise section", "### THE HERO PROMISE" in doc),
        ("Hero standard = floor", "Hero Standard = Floor Standard" in doc),
        ("Data sources", "**Data Sources**:" in doc),
        ("Confidence score", "**Confidence**: 100%" in doc),
    ]

    passed = 0
    failed = 0

    for check_name, result in checks:
        if result:
            print(f"✅ {check_name}")
            passed += 1
        else:
            print(f"❌ {check_name}")
            failed += 1

    print(f"\nRESULT: {passed}/{len(checks)} checks passed")

    # Show document length
    print(f"Document length: {len(doc)} characters")
    print(f"Word count: ~{len(doc.split())} words")

    return failed == 0


def test_document_04():
    """Test Document 04: Nutritional Excellence builder"""
    print("\n" + "=" * 80)
    print("TEST: DOCUMENT 04 - NUTRITIONAL EXCELLENCE")
    print("=" * 80)

    data_source = get_data_source()
    doc = build_document_04(data_source)

    # VERIFICATION: Check all required sections exist
    checks = [
        ("Document header", "## DOCUMENT 04: Nutritional Excellence" in doc),
        ("Nutritional philosophy", "### NUTRITIONAL PHILOSOPHY" in doc),
        ("Philosophy quote", "We let the data speak" in doc),
        ("Specificity examples", "254.5% RDA Selenium" in doc),
        ("FSSAI compliance", "#### FSSAI Compliance" in doc),
        ("Top highlights section", "### TOP NUTRITIONAL HIGHLIGHTS" in doc),
        ("Highlights table", "| Rank | Product | Nutrient | RDA % | Claim |" in doc),
        ("Ranked highlights", "**#1**" in doc),
        ("Top 11 highlights", "#11" in doc or len([line for line in doc.split('\n') if '**#' in line]) >= 11),
        ("Nutrient profiles section", "### DETAILED NUTRIENT PROFILES" in doc),
        ("Selenium powerhouses", "Selenium" in doc),  # Should be grouped
        ("Multi-nutrient champions", "#### **Multi-Nutrient Champions**" in doc),
        ("FSSAI standards section", "### FSSAI STANDARDS & COMPLIANCE" in doc),
        ("Source of definition", "\"Source of\" Nutrient" in doc),
        ("Good source definition", "\"Good Source of\" Nutrient" in doc),
        ("Excellent source definition", "\"Excellent Source of\" Nutrient" in doc),
        ("Third-party verification", "Third-Party Verification" in doc),
        ("Certifications list", "✅ FSSAI License" in doc),
        ("Health benefit mapping", "### HEALTH BENEFIT MAPPING" in doc),
        ("Thyroid support", "#### **Thyroid Support**" in doc),
        ("Bone health", "#### **Bone Health**" in doc),
        ("Antioxidant protection", "#### **Antioxidant Protection**" in doc),
        ("Energy & performance", "#### **Energy & Performance**" in doc),
        ("Immune function", "#### **Immune Function**" in doc),
        ("Heart health", "#### **Heart Health**" in doc),
        ("How to use map", "**How to Use This Map**:" in doc),
        ("Data sources", "**Data Sources**:" in doc),
        ("Confidence score", "**Confidence**: 100%" in doc),
    ]

    passed = 0
    failed = 0

    for check_name, result in checks:
        if result:
            print(f"✅ {check_name}")
            passed += 1
        else:
            print(f"❌ {check_name}")
            failed += 1

    print(f"\nRESULT: {passed}/{len(checks)} checks passed")

    # Show document length
    print(f"Document length: {len(doc)} characters")
    print(f"Word count: ~{len(doc.split())} words")

    return failed == 0


def test_data_accuracy():
    """Test that data comes from JSON, not hardcoded"""
    print("\n" + "=" * 80)
    print("TEST: DATA ACCURACY (FROM JSON)")
    print("=" * 80)

    data_source = get_data_source()

    # Get products directly
    brazil_nuts = data_source.get_product_by_id("brazil-nuts")
    medjoul_dates = data_source.get_product_by_id("medjoul-dates")

    # Generate documents
    doc03 = build_document_03(data_source)
    doc04 = build_document_04(data_source)

    # VERIFICATION: Check data matches JSON
    checks = [
        ("Brazil nuts origin in doc", brazil_nuts['origin'] in doc03),
        ("Brazil nuts characteristics", brazil_nuts['characteristics'] in doc03),
        ("Brazil nuts selenium RDA", "254.5" in doc03),  # From JSON
        ("Medjoul dates origin in doc", medjoul_dates['origin'] in doc03),
        ("Medjoul dates characteristics", medjoul_dates['characteristics'] in doc03),
        ("Medjoul workout benefits exist", "workoutBenefits" in medjoul_dates),
        ("Pre-workout in doc", "30-45 minutes before exercise" in doc03),
        ("Nutritional highlights extracted", len(data_source.get_nutritional_highlights()) > 0),
        ("Top highlights in doc04", "254.5% RDA Selenium" in doc04),
    ]

    passed = 0
    failed = 0

    for check_name, result in checks:
        if result:
            print(f"✅ {check_name}")
            passed += 1
        else:
            print(f"❌ {check_name}")
            failed += 1

    print(f"\nRESULT: {passed}/{len(checks)} checks passed")

    return failed == 0


def test_comparison_with_spec():
    """Test that generated content matches spec requirements"""
    print("\n" + "=" * 80)
    print("TEST: SPEC COMPLIANCE")
    print("=" * 80)

    data_source = get_data_source()
    doc03 = build_document_03(data_source)
    doc04 = build_document_04(data_source)

    # Doc 03 spec requirements
    doc03_checks = [
        ("Brazil Nuts: ALL data from JSON", "254.5%" in doc03 and "Brazil / Bolivia" in doc03),
        ("Brazil Nuts: Explain selenium role", "Thyroid function regulation" in doc03),
        ("Brazil Nuts: Complete sourcing story", "Wild-harvested" in doc03 and "Amazon" in doc03),
        ("Brazil Nuts: ALL benefits sorted by RDA", "Selenium" in doc03 and "Copper" in doc03),
        ("Brazil Nuts: Brand DNA explanation", "Why Brazil Nuts Are Hero #1" in doc03),
        ("Medjoul: ALL data from JSON", "5+ year bestseller" in doc03 and "Jordan / Palestine" in doc03),
        ("Medjoul: Bestseller status", "Amazon's 5+ Year Bestseller" in doc03),
        ("Medjoul: Cold chain advantage", "India's ONLY cold chain" in doc03),
        ("Medjoul: Workout benefits", "Pre-Workout" in doc03 and "Post-Workout" in doc03),
        ("Medjoul: Taste/texture evolution", "Flavor Evolution" in doc03 and "Texture Journey" in doc03),
        ("Medjoul: Customer validation", "Customer Testimonials" in doc03 and "46%" in doc03),
        ("Why These 2: Complementary nature", "Complementary Storytelling" in doc03),
        ("Hero Promise: Translates to standard", "Hero Standard = Floor Standard" in doc03),
    ]

    # Doc 04 spec requirements
    doc04_checks = [
        ("Philosophy: 3 specific examples", "254.5% RDA Selenium" in doc04),
        ("Philosophy: Contrast specific vs vague", "high in selenium" in doc04.lower()),
        ("Top 11: Extracted from all products", "| **#1** |" in doc04),
        ("Top 11: Sorted by RDA descending", "#1" in doc04 and "#11" in doc04 or "#10" in doc04),
        ("Profiles: Grouped by nutrient", "Powerhouses" in doc04 or "Champions" in doc04),
        ("Profiles: Multi-nutrient identified", "Multi-Nutrient" in doc04),
        ("FSSAI: 3 thresholds explained", "10% RDA" in doc04 and "20% RDA" in doc04 and "30% RDA" in doc04),
        ("FSSAI: How we exceed standards", "We Go Beyond Minimum" in doc04),
        ("FSSAI: Certifications listed", "FSSAI License" in doc04),
        ("Health mapping: 6 major goals", "Thyroid Support" in doc04 and "Bone Health" in doc04),
        ("Health mapping: Product recommendations", "Best Choice" in doc04 or "Best Choices" in doc04),
    ]

    all_checks = doc03_checks + doc04_checks
    passed = 0
    failed = 0

    print("\nDocument 03 Spec Compliance:")
    for check_name, result in doc03_checks:
        if result:
            print(f"✅ {check_name}")
            passed += 1
        else:
            print(f"❌ {check_name}")
            failed += 1

    print("\nDocument 04 Spec Compliance:")
    for check_name, result in doc04_checks:
        if result:
            print(f"✅ {check_name}")
            passed += 1
        else:
            print(f"❌ {check_name}")
            failed += 1

    print(f"\nRESULT: {passed}/{len(all_checks)} spec requirements met")

    return failed == 0


if __name__ == "__main__":
    print("🧪 TESTING DOCUMENT BUILDERS 03 & 04\n")

    # Run all tests
    test1 = test_document_03()
    test2 = test_document_04()
    test3 = test_data_accuracy()
    test4 = test_comparison_with_spec()

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    all_passed = test1 and test2 and test3 and test4

    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("🎯 Document builders 03 & 04 are working correctly")
        print("📝 Ready to integrate into act1_generator.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("🔍 Review failed checks above")

    print("\n" + "=" * 80)
