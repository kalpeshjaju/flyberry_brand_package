#!/usr/bin/env python3
"""
Product Validation Test Suite - Flyberry Brand Package
Tests the actual product functionality and output quality
Date: October 24, 2025
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import subprocess

# Add paths
sys.path.insert(0, '/Users/kalpeshjaju/Development/flyberry_oct_restart')
sys.path.insert(0, '/Users/kalpeshjaju/Development/flyberry_brand_package')

# Colors for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'  # No Color

print(f"{CYAN}{'='*70}{NC}")
print(f"{CYAN}PRODUCT VALIDATION TEST SUITE{NC}")
print(f"{CYAN}Testing actual product functionality and output quality{NC}")
print(f"{CYAN}{'='*70}{NC}")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Test results tracking
test_results = {
    "build": [],
    "content": [],
    "navigation": [],
    "data": [],
    "user_experience": []
}

def log_test(category, test_name, status, details=""):
    """Log test result"""
    symbol = "✅" if status == "PASS" else "❌"
    color = GREEN if status == "PASS" else RED
    print(f"  {color}{symbol} {test_name}{NC}")
    if details:
        print(f"     {details}")
    test_results[category].append({
        "test": test_name,
        "status": status,
        "details": details
    })

# ============ SECTION 1: FRESH BUILD TEST ============
print(f"\n{YELLOW}=== SECTION 1: Fresh Build Test ==={NC}")
print("Generating fresh HTML output...\n")

def test_fresh_build():
    """Perform a fresh build and validate output"""
    os.chdir('/Users/kalpeshjaju/Development/flyberry_brand_package')

    # Clean previous build (preserve index.html)
    print("  Cleaning previous build...")
    docs_path = Path("docs")
    for html_file in docs_path.glob("*.html"):
        if html_file.name != "index.html":  # Preserve index.html
            html_file.unlink()

    # Run build
    print("  Running build process...")
    result = subprocess.run(
        ["python3", "build.py"],
        input="1\n",  # Continue with gaps
        capture_output=True,
        text=True
    )

    # Check if build succeeded
    if "Build complete!" in result.stdout:
        log_test("build", "Build Process", "PASS", "Build completed successfully")
    else:
        log_test("build", "Build Process", "FAIL", "Build did not complete")
        return False

    # Verify all HTML files generated (index.html is manually created)
    expected_generated_files = [
        "act-1-who-we-are.html",
        "act-2-where-we-are.html",
        "act-3-discoveries.html",
        "act-4-market-proof.html",
        "act-5-where-to-go.html"
    ]

    for file_name in expected_generated_files:
        file_path = docs_path / file_name
        if file_path.exists() and file_path.stat().st_size > 1000:
            log_test("build", f"Generate {file_name}", "PASS", f"Size: {file_path.stat().st_size:,} bytes")
        else:
            log_test("build", f"Generate {file_name}", "FAIL", "File missing or too small")

    # Check index.html separately (manually created navigation)
    index_path = docs_path / "index.html"
    if index_path.exists() and index_path.stat().st_size > 1000:
        log_test("build", "Index navigation page", "PASS", f"Size: {index_path.stat().st_size:,} bytes")
    else:
        log_test("build", "Index navigation page", "WARN", "Missing - manually created file")

    return True

test_fresh_build()

# ============ SECTION 2: CONTENT ACCURACY TEST ============
print(f"\n{YELLOW}=== SECTION 2: Content Accuracy Test ==={NC}")
print("Validating HTML content matches source data...\n")

def test_content_accuracy():
    """Validate that HTML content matches JSON data"""
    from flyberry_data_loader import FlyberryData

    # Load source data
    data = FlyberryData(data_dir="/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data")

    # Test Act 1 - Product Data
    act1_path = Path("docs/act-1-who-we-are.html")
    with open(act1_path, 'r', encoding='utf-8') as f:
        act1_html = f.read()

    soup = BeautifulSoup(act1_html, 'html.parser')

    # Check if key products are mentioned
    key_products = ["Medjoul Dates", "Ajwa Dates", "Brazil Nuts", "Macadamia Nuts"]
    for product_name in key_products:
        if product_name in act1_html:
            log_test("content", f"Product: {product_name}", "PASS", "Found in Act 1")
        else:
            log_test("content", f"Product: {product_name}", "FAIL", "Missing from Act 1")

    # Check product count
    product_count_match = re.search(r'(\d+)\s*(?:premium\s+)?products?', act1_html.lower())
    if product_count_match:
        count_in_html = int(product_count_match.group(1))
        actual_count = len(data.products)
        if abs(count_in_html - actual_count) <= 1:  # Allow slight variation
            log_test("content", "Product Count", "PASS", f"HTML: {count_in_html}, Data: {actual_count}")
        else:
            log_test("content", "Product Count", "FAIL", f"HTML: {count_in_html}, Data: {actual_count}")

    # Check brand name
    if "Flyberry" in act1_html:
        log_test("content", "Brand Name", "PASS", "Flyberry brand name present")
    else:
        log_test("content", "Brand Name", "FAIL", "Brand name missing")

    # Check for key sections
    key_sections = [
        "Origin Story",
        "Product Portfolio",
        "Brand Promise"
    ]

    for section in key_sections:
        if section.lower() in act1_html.lower():
            log_test("content", f"Section: {section}", "PASS", "Section found")
        else:
            log_test("content", f"Section: {section}", "FAIL", "Section missing")

test_content_accuracy()

# ============ SECTION 3: NAVIGATION TEST ============
print(f"\n{YELLOW}=== SECTION 3: Navigation & Links Test ==={NC}")
print("Testing navigation between pages...\n")

def test_navigation():
    """Test navigation links and structure"""
    docs_path = Path("docs")

    # Test index page links
    index_path = docs_path / "index.html"
    with open(index_path, 'r', encoding='utf-8') as f:
        index_html = f.read()

    soup = BeautifulSoup(index_html, 'html.parser')

    # Find all Act links
    act_links = soup.find_all('a', href=re.compile(r'act-\d'))
    if len(act_links) >= 5:
        log_test("navigation", "Index Page Links", "PASS", f"Found {len(act_links)} Act links")
    else:
        log_test("navigation", "Index Page Links", "FAIL", f"Only {len(act_links)} Act links found")

    # Test each Act page has navigation
    for act_num in range(1, 6):
        act_file = f"act-{act_num}-*.html"
        act_files = list(docs_path.glob(act_file))
        if act_files:
            act_path = act_files[0]
            with open(act_path, 'r', encoding='utf-8') as f:
                act_html = f.read()

            # Check for navigation elements
            has_nav = 'nav' in act_html.lower()
            has_home_link = 'index.html' in act_html or 'home' in act_html.lower()

            if has_nav and has_home_link:
                log_test("navigation", f"Act {act_num} Navigation", "PASS", "Has nav and home link")
            else:
                log_test("navigation", f"Act {act_num} Navigation", "FAIL", "Missing navigation")

    # Check for consistent header/footer
    for html_file in docs_path.glob("act-*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        has_header = '<header' in html_content
        has_proper_structure = '<!DOCTYPE html>' in html_content

        if has_header and has_proper_structure:
            log_test("navigation", f"{html_file.name} Structure", "PASS", "Valid HTML structure")
        else:
            log_test("navigation", f"{html_file.name} Structure", "FAIL", "Invalid structure")
            break

test_navigation()

# ============ SECTION 4: DATA REPRESENTATION TEST ============
print(f"\n{YELLOW}=== SECTION 4: Data Representation Test ==={NC}")
print("Verifying data is accurately displayed...\n")

def test_data_representation():
    """Test that data from JSON appears correctly in HTML"""
    from flyberry_data_loader import FlyberryData

    # Load source data
    data = FlyberryData(data_dir="/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data")

    # Get a specific product for detailed testing
    medjoul = data.get_product("medjoul-dates")

    # Load Act 1 HTML
    act1_path = Path("docs/act-1-who-we-are.html")
    with open(act1_path, 'r', encoding='utf-8') as f:
        act1_html = f.read()

    # Test specific product details
    if medjoul:
        # Check product name
        if medjoul['name'] in act1_html:
            log_test("data", "Medjoul Name", "PASS", f"Found: {medjoul['name']}")
        else:
            log_test("data", "Medjoul Name", "FAIL", "Product name not found")

        # Check origin
        if medjoul.get('origin', '') and medjoul['origin'] in act1_html:
            log_test("data", "Medjoul Origin", "PASS", f"Found: {medjoul['origin']}")
        else:
            log_test("data", "Medjoul Origin", "FAIL", "Origin not displayed")

        # Check tagline
        if medjoul.get('tagline', '') and medjoul['tagline'] in act1_html:
            log_test("data", "Medjoul Tagline", "PASS", "Tagline displayed")
        else:
            log_test("data", "Medjoul Tagline", "WARN", "Tagline might be missing")

    # Test recipe data in Act 3
    act3_path = Path("docs/act-3-discoveries.html")
    if act3_path.exists():
        with open(act3_path, 'r', encoding='utf-8') as f:
            act3_html = f.read()

        # Check if recipes are mentioned
        recipe_count = len(data.recipes)
        if str(recipe_count) in act3_html or "recipe" in act3_html.lower():
            log_test("data", "Recipe Data", "PASS", f"{recipe_count} recipes in system")
        else:
            log_test("data", "Recipe Data", "WARN", "Recipes might not be displayed")

    # Test financial data in Act 2
    act2_path = Path("docs/act-2-where-we-are.html")
    if act2_path.exists():
        with open(act2_path, 'r', encoding='utf-8') as f:
            act2_html = f.read()

        # Check for financial indicators
        financial_terms = ["revenue", "growth", "performance", "FY", "quarter"]
        found_terms = [term for term in financial_terms if term.lower() in act2_html.lower()]

        if len(found_terms) >= 2:
            log_test("data", "Financial Data", "PASS", f"Found: {', '.join(found_terms)}")
        else:
            log_test("data", "Financial Data", "FAIL", "Missing financial information")

    # Test customer segments
    if hasattr(data, 'customer_segments') and data.customer_segments:
        segment_count = len(data.customer_segments.get('segments', []))
        if segment_count > 0:
            log_test("data", "Customer Segments", "PASS", f"{segment_count} segments loaded")
        else:
            log_test("data", "Customer Segments", "WARN", "No segments found")

test_data_representation()

# ============ SECTION 5: USER EXPERIENCE TEST ============
print(f"\n{YELLOW}=== SECTION 5: User Experience Test ==={NC}")
print("Testing overall user experience...\n")

def test_user_experience():
    """Test the overall user experience"""
    docs_path = Path("docs")

    # Test CSS is applied
    css_path = docs_path / "assets" / "css" / "styles.css"
    if css_path.exists():
        log_test("user_experience", "CSS Styles", "PASS", "Stylesheet present")

        # Check if CSS is linked in HTML
        act1_path = docs_path / "act-1-who-we-are.html"
        with open(act1_path, 'r', encoding='utf-8') as f:
            html = f.read()

        if 'styles.css' in html:
            log_test("user_experience", "CSS Linked", "PASS", "Styles properly linked")
        else:
            log_test("user_experience", "CSS Linked", "FAIL", "CSS not linked to HTML")
    else:
        log_test("user_experience", "CSS Styles", "FAIL", "No stylesheet found")

    # Test readability
    act1_path = docs_path / "act-1-who-we-are.html"
    with open(act1_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Check for proper heading hierarchy
    h1_tags = soup.find_all('h1')
    h2_tags = soup.find_all('h2')

    if len(h1_tags) >= 1 and len(h2_tags) >= 1:
        log_test("user_experience", "Heading Structure", "PASS", f"{len(h1_tags)} H1, {len(h2_tags)} H2 tags")
    else:
        log_test("user_experience", "Heading Structure", "FAIL", "Poor heading hierarchy")

    # Check for proper formatting
    paragraphs = soup.find_all('p')
    lists = soup.find_all(['ul', 'ol'])

    if len(paragraphs) > 5 and len(lists) > 0:
        log_test("user_experience", "Content Formatting", "PASS", f"{len(paragraphs)} paragraphs, {len(lists)} lists")
    else:
        log_test("user_experience", "Content Formatting", "FAIL", "Insufficient formatting")

    # Test page load size (should be reasonable)
    total_size = 0
    for html_file in docs_path.glob("*.html"):
        total_size += html_file.stat().st_size

    total_mb = total_size / (1024 * 1024)
    if total_mb < 5:  # Less than 5MB total
        log_test("user_experience", "Page Size", "PASS", f"Total: {total_mb:.2f}MB - Good for web")
    else:
        log_test("user_experience", "Page Size", "WARN", f"Total: {total_mb:.2f}MB - May be slow")

    # Test metadata
    if '<meta name="viewport"' in html_content:
        log_test("user_experience", "Mobile Support", "PASS", "Viewport meta tag present")
    else:
        log_test("user_experience", "Mobile Support", "FAIL", "No viewport meta tag")

    if '<title>' in html_content:
        log_test("user_experience", "Page Title", "PASS", "Title tag present")
    else:
        log_test("user_experience", "Page Title", "FAIL", "No title tag")

test_user_experience()

# ============ SECTION 6: REFERENCE DATA SYSTEM TEST ============
print(f"\n{YELLOW}=== SECTION 6: Reference Data System Test ==={NC}")
print("Testing reference data handling...\n")

def test_reference_system():
    """Test how the system handles reference data"""
    from data_integration import BrandPackageDataSource

    data_source = BrandPackageDataSource()

    # Check missing data detection
    missing = data_source.check_data_completeness()

    if missing:
        log_test("user_experience", "Missing Data Detection", "PASS", f"Detected {len(missing)} missing files")

        # Verify it's the expected missing files
        expected_missing = [
            "customer-testimonials-reference.json",
            "market-trends-reference.json",
            "market-size-reference.json",
            "market-validation-reference.json",
            "trend-analysis-reference.json",
            "expansion-opportunities-reference.json"
        ]

        missing_files = [item['file'] for item in missing]

        for expected in expected_missing:
            if expected in missing_files:
                log_test("user_experience", f"Track {expected[:20]}...", "PASS", "Correctly identified as missing")
    else:
        log_test("user_experience", "Missing Data Detection", "INFO", "All reference data present")

    # Test existing reference file
    ref_files = data_source.list_reference_files()
    if ref_files:
        log_test("user_experience", "Reference Files", "PASS", f"Found {len(ref_files)} reference file(s)")
        for ref in ref_files[:2]:  # Show first 2
            print(f"     - {ref['file']}: {ref.get('confidence', 'unknown')} confidence")

test_reference_system()

# ============ GENERATE REPORT ============
print(f"\n{CYAN}{'='*70}{NC}")
print(f"{CYAN}PRODUCT TEST SUMMARY{NC}")
print(f"{CYAN}{'='*70}{NC}\n")

# Calculate statistics
total_tests = sum(len(tests) for tests in test_results.values())
passed_tests = sum(len([t for t in tests if t['status'] == 'PASS']) for tests in test_results.values())
failed_tests = sum(len([t for t in tests if t['status'] == 'FAIL']) for tests in test_results.values())
warning_tests = sum(len([t for t in tests if t['status'] == 'WARN']) for tests in test_results.values())

print(f"Total Tests: {total_tests}")
print(f"{GREEN}Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%){NC}")
print(f"{RED}Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%){NC}")
print(f"{YELLOW}Warnings: {warning_tests}{NC}")

print(f"\n{BLUE}Category Breakdown:{NC}")
for category, tests in test_results.items():
    passed = len([t for t in tests if t['status'] == 'PASS'])
    total = len(tests)
    status_color = GREEN if passed == total else YELLOW if passed/total > 0.7 else RED
    print(f"  {category.title()}: {status_color}{passed}/{total} passed{NC}")

# Overall verdict
print(f"\n{CYAN}{'='*70}{NC}")
if passed_tests / total_tests >= 0.9:
    print(f"{GREEN}✅ PRODUCT VALIDATION: PASSED{NC}")
    print("The Flyberry Brand Package is working as expected!")
elif passed_tests / total_tests >= 0.7:
    print(f"{YELLOW}⚠️  PRODUCT VALIDATION: MOSTLY PASSING{NC}")
    print("The product is functional with some minor issues.")
else:
    print(f"{RED}❌ PRODUCT VALIDATION: NEEDS ATTENTION{NC}")
    print("Several issues need to be addressed.")
print(f"{CYAN}{'='*70}{NC}")

# Save detailed report
report = {
    "timestamp": datetime.now().isoformat(),
    "summary": {
        "total_tests": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "warnings": warning_tests,
        "pass_rate": passed_tests / total_tests * 100
    },
    "categories": test_results,
    "verdict": "PASSED" if passed_tests / total_tests >= 0.9 else "NEEDS_ATTENTION"
}

with open("PRODUCT_TEST_REPORT.json", 'w') as f:
    json.dump(report, f, indent=2)

print(f"\n📄 Detailed report saved to: PRODUCT_TEST_REPORT.json")
print(f"📂 HTML output available at: docs/index.html")
print("\nTo view the product, open: file:///Users/kalpeshjaju/Development/flyberry_brand_package/docs/index.html")