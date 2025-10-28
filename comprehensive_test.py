#!/usr/bin/env python3
"""
Comprehensive Test Suite for Flyberry Brand Package System
Date: October 24, 2025
Purpose: Validate all components with updated tech stack
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime

# Colors for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

# Test results tracking
test_results = []
total_tests = 0
passed_tests = 0
failed_tests = 0

def test_case(name, description):
    """Decorator for test cases"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            global total_tests, passed_tests, failed_tests
            total_tests += 1
            print(f"\n{BLUE}[TEST {total_tests}]{NC} {name}")
            print(f"  Description: {description}")

            try:
                result = func(*args, **kwargs)
                if result:
                    print(f"  {GREEN}✅ PASS{NC}")
                    passed_tests += 1
                    test_results.append({"test": name, "status": "PASS", "details": ""})
                else:
                    print(f"  {RED}❌ FAIL{NC}")
                    failed_tests += 1
                    test_results.append({"test": name, "status": "FAIL", "details": "Returned False"})
                return result
            except Exception as e:
                print(f"  {RED}❌ FAIL: {str(e)}{NC}")
                failed_tests += 1
                test_results.append({"test": name, "status": "FAIL", "details": str(e)})
                return False
        return wrapper
    return decorator

print(f"{GREEN}{'='*60}{NC}")
print(f"{GREEN}COMPREHENSIVE TEST SUITE - FLYBERRY BRAND PACKAGE{NC}")
print(f"{GREEN}{'='*60}{NC}")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Python Version: {sys.version.split()[0]}")

# ========== PACKAGE VERSION TESTS ==========
print(f"\n{YELLOW}=== SECTION 1: Package Version Tests ==={NC}")

@test_case("Package Versions", "Verify all packages are at expected versions")
def test_package_versions():
    """Test that all required packages are installed with correct versions"""
    import importlib

    packages = [
        ('markdown', '3.9', '3.4.0'),
        ('jinja2', '3.1.6', '3.1.0'),
        ('anthropic', '0.71.0', '0.30.0')
    ]

    all_good = True
    for pkg_name, expected, minimum in packages:
        try:
            pkg = importlib.import_module(pkg_name)
            version = getattr(pkg, '__version__', 'unknown')
            print(f"    {pkg_name}: {version} (min: {minimum})")

            # Basic version check
            if version < minimum:
                print(f"    {RED}⚠️  {pkg_name} version {version} is below minimum {minimum}{NC}")
                all_good = False
        except ImportError:
            print(f"    {RED}❌ {pkg_name} not installed{NC}")
            all_good = False

    return all_good

# ========== DATA SOURCE TESTS ==========
print(f"\n{YELLOW}=== SECTION 2: Data Source Tests ==={NC}")

# Add flyberry_oct_restart to path
sys.path.insert(0, '/Users/kalpeshjaju/Development/flyberry_oct_restart')
sys.path.insert(0, '/Users/kalpeshjaju/Development/flyberry_brand_package')

@test_case("Data Directory Structure", "Verify flyberry_oct_restart structure is intact")
def test_data_structure():
    """Test that all required data directories exist"""
    base_path = Path("/Users/kalpeshjaju/Development/flyberry_oct_restart")

    required_dirs = [
        "raw_data",
        "raw_data/references",
        "llm_readable",
        "extracted_data",
        "extracted_data/products",
        "extracted_data/recipes",
        "extracted_data/design",
        "extracted_data/schemas"
    ]

    all_exist = True
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"    ✅ {dir_name}")
        else:
            print(f"    ❌ {dir_name} - NOT FOUND")
            all_exist = False

    return all_exist

@test_case("Data Loading", "Load data using FlyberryData class")
def test_data_loading():
    """Test the main data loader functionality"""
    try:
        from flyberry_data_loader import FlyberryData

        # Initialize with correct path
        data = FlyberryData(data_dir="/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data")

        # Check products
        products_count = len(data.products)
        print(f"    Products loaded: {products_count}")

        # Check recipes
        recipes_count = len(data.recipes)
        print(f"    Recipes loaded: {recipes_count}")

        # Check claims
        claims_count = len(data.claims.get('claims', []))
        print(f"    Claims loaded: {claims_count}")

        # Validate counts
        return products_count == 13 and recipes_count == 11

    except Exception as e:
        print(f"    Error: {e}")
        return False

@test_case("Data Lineage", "Verify data lineage tracking")
def test_data_lineage():
    """Test that data lineage file exists and is valid"""
    lineage_file = Path("/Users/kalpeshjaju/Development/flyberry_oct_restart/data-lineage.json")

    if not lineage_file.exists():
        print(f"    ❌ data-lineage.json not found")
        return False

    try:
        with open(lineage_file, 'r') as f:
            lineage_data = json.load(f)

        # Check for metadata
        if 'metadata' not in lineage_data:
            print(f"    ❌ Missing metadata in lineage file")
            return False

        # Check for reference data policy
        if 'referenceDataPolicy' in lineage_data['metadata']:
            print(f"    ✅ Reference data policy configured")

        # Count entries
        entries = len([k for k in lineage_data.keys() if k != 'metadata'])
        print(f"    Total lineage entries: {entries}")

        # Check for reference tracking
        ref_entries = [k for k in lineage_data.keys() if '-reference.json' in k]
        print(f"    Reference data entries: {len(ref_entries)}")

        return True

    except Exception as e:
        print(f"    Error reading lineage: {e}")
        return False

# ========== INTEGRATION TESTS ==========
print(f"\n{YELLOW}=== SECTION 3: Integration Tests ==={NC}")

@test_case("Data Integration", "Test data_integration.py module")
def test_data_integration():
    """Test the data integration module"""
    try:
        from data_integration import BrandPackageDataSource

        # Initialize data source
        data_source = BrandPackageDataSource()

        # Test product loading
        products = data_source.get_all_products()
        print(f"    Products accessible: {len(products)}")

        # Test recipes loading
        recipes = data_source.get_all_recipes()
        print(f"    Recipes accessible: {len(recipes)}")

        # Test brand info
        brand_info = data_source.get_brand_info()
        print(f"    Brand name: {brand_info.get('name', 'NOT FOUND')}")

        return len(products) == 13 and len(recipes) == 11

    except Exception as e:
        print(f"    Error: {e}")
        return False

@test_case("Reference Data System", "Test reference data detection")
def test_reference_system():
    """Test the reference data completeness checker"""
    try:
        from data_integration import BrandPackageDataSource

        data_source = BrandPackageDataSource()

        # Check for missing data
        missing_data = data_source.check_data_completeness()
        print(f"    Missing reference files: {len(missing_data)}")

        if missing_data:
            print(f"    Missing files by Act:")
            acts = {}
            for item in missing_data:
                act = item['act']
                if act not in acts:
                    acts[act] = 0
                acts[act] += 1

            for act, count in sorted(acts.items()):
                print(f"      {act}: {count} files")

        # Check if reference files can be listed
        ref_files = data_source.list_reference_files()
        print(f"    Existing reference files: {len(ref_files)}")

        return True  # System works even with missing files

    except Exception as e:
        print(f"    Error: {e}")
        return False

# ========== GENERATOR TESTS ==========
print(f"\n{YELLOW}=== SECTION 4: Generator Tests ==={NC}")

@test_case("Anti-Hallucination Validator", "Test hallucination detection")
def test_anti_hallucination():
    """Test the anti-hallucination validation system"""
    try:
        from generators.anti_hallucination_validator import HallucinationValidator

        gen_dir = Path("/Users/kalpeshjaju/Development/flyberry_brand_package/generators")
        validator = HallucinationValidator(gen_dir)

        # Run validation
        is_clean = validator.validate_all()

        if is_clean:
            print(f"    ✅ No hallucinations detected")
        else:
            print(f"    ❌ Hallucinations found:")
            for issue in validator.issues_found[:3]:  # Show first 3 issues
                print(f"      - {issue}")

        return is_clean

    except Exception as e:
        print(f"    Error: {e}")
        return False

@test_case("Markdown Processing", "Test markdown to HTML conversion")
def test_markdown_processing():
    """Test markdown processing with the updated package"""
    try:
        import markdown

        # Create markdown instance
        md = markdown.Markdown(extensions=['extra', 'meta'])

        # Test simple conversion
        test_md = """# Test Header

## Subheader

- List item 1
- List item 2

**Bold text** and *italic text*

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
"""

        html = md.convert(test_md)

        # Check if conversion worked
        has_h1 = '<h1>' in html
        has_table = '<table>' in html
        has_list = '<ul>' in html or '<li>' in html

        print(f"    Markdown version: {markdown.__version__}")
        print(f"    H1 conversion: {'✅' if has_h1 else '❌'}")
        print(f"    Table support: {'✅' if has_table else '❌'}")
        print(f"    List support: {'✅' if has_list else '❌'}")

        return has_h1 and has_list

    except Exception as e:
        print(f"    Error: {e}")
        return False

@test_case("Jinja2 Template Rendering", "Test template engine")
def test_jinja2_rendering():
    """Test Jinja2 template rendering"""
    try:
        from jinja2 import Environment, FileSystemLoader, Template
        import jinja2

        # Test simple template
        template_str = """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ heading }}</h1>
    {% for item in items %}
    <p>{{ item }}</p>
    {% endfor %}
</body>
</html>
"""

        template = Template(template_str)
        html = template.render(
            title="Test Page",
            heading="Test Heading",
            items=["Item 1", "Item 2", "Item 3"]
        )

        # Verify rendering
        has_title = "Test Page" in html
        has_items = "Item 1" in html and "Item 2" in html

        print(f"    Jinja2 version: {jinja2.__version__}")
        print(f"    Template rendering: {'✅' if has_title else '❌'}")
        print(f"    Loop rendering: {'✅' if has_items else '❌'}")

        return has_title and has_items

    except Exception as e:
        print(f"    Error: {e}")
        return False

# ========== BUILD PIPELINE TESTS ==========
print(f"\n{YELLOW}=== SECTION 5: Build Pipeline Tests ==={NC}")

@test_case("Build Script Import", "Test build.py can be imported")
def test_build_imports():
    """Test that build script and its dependencies load"""
    try:
        # Change to correct directory
        os.chdir('/Users/kalpeshjaju/Development/flyberry_brand_package')

        # Try importing key functions
        from build import generate_research_tasks, build_act

        print(f"    ✅ Build functions imported successfully")
        return True

    except Exception as e:
        print(f"    Error importing build: {e}")
        return False

@test_case("Generator Modules", "Test all generator modules load")
def test_generators():
    """Test that all generator modules can be imported"""
    try:
        generators = [
            'act1_generator',
            'act2_generator',
            'act3_generator',
            'act4_generator',
            'document_builders_01_02',
            'document_builders_03_04',
            'document_builders_05_06'
        ]

        all_loaded = True
        for gen in generators:
            try:
                module = __import__(f'generators.{gen}', fromlist=[''])
                print(f"    ✅ {gen}")
            except Exception as e:
                print(f"    ❌ {gen}: {e}")
                all_loaded = False

        return all_loaded

    except Exception as e:
        print(f"    Error: {e}")
        return False

# ========== OUTPUT TESTS ==========
print(f"\n{YELLOW}=== SECTION 6: Output Validation Tests ==={NC}")

@test_case("HTML Output Files", "Verify HTML files exist")
def test_html_output():
    """Test that HTML output files exist"""
    output_dir = Path("/Users/kalpeshjaju/Development/flyberry_brand_package/docs")

    required_files = [
        "index.html",
        "act-1-who-we-are.html",
        "act-2-where-we-are.html",
        "act-3-discoveries.html",
        "act-4-market-proof.html",
        "act-5-where-to-go.html"
    ]

    all_exist = True
    for file_name in required_files:
        file_path = output_dir / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"    ✅ {file_name} ({size:,} bytes)")
        else:
            print(f"    ❌ {file_name} - NOT FOUND")
            all_exist = False

    return all_exist

@test_case("Asset Files", "Verify CSS and image assets")
def test_assets():
    """Test that asset files are properly copied"""
    assets_dir = Path("/Users/kalpeshjaju/Development/flyberry_brand_package/docs/assets")

    if not assets_dir.exists():
        print(f"    ❌ Assets directory not found")
        return False

    # Check for CSS
    css_dir = assets_dir / "css"
    if css_dir.exists():
        css_files = list(css_dir.glob("*.css"))
        print(f"    CSS files: {len(css_files)}")
    else:
        print(f"    ❌ CSS directory not found")
        return False

    # Check for images
    img_dir = assets_dir / "images"
    if img_dir.exists():
        print(f"    ✅ Images directory exists")
    else:
        print(f"    ⚠️  Images directory not found (may be empty)")

    return css_dir.exists()

# ========== PERFORMANCE TESTS ==========
print(f"\n{YELLOW}=== SECTION 7: Performance Tests ==={NC}")

@test_case("Data Loading Speed", "Measure data loading performance")
def test_loading_performance():
    """Test data loading performance"""
    try:
        from flyberry_data_loader import FlyberryData
        import time

        start_time = time.time()
        data = FlyberryData(data_dir="/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data")
        load_time = time.time() - start_time

        print(f"    Load time: {load_time:.3f} seconds")
        print(f"    Performance: {'✅ Excellent' if load_time < 1 else '⚠️ Acceptable' if load_time < 3 else '❌ Slow'}")

        return load_time < 3  # Should load in under 3 seconds

    except Exception as e:
        print(f"    Error: {e}")
        return False

# ========== TEST EXECUTION ==========

def run_all_tests():
    """Execute all test cases"""

    # Run all tests (they auto-execute when defined with decorator)
    test_package_versions()
    test_data_structure()
    test_data_loading()
    test_data_lineage()
    test_data_integration()
    test_reference_system()
    test_anti_hallucination()
    test_markdown_processing()
    test_jinja2_rendering()
    test_build_imports()
    test_generators()
    test_html_output()
    test_assets()
    test_loading_performance()

    # Generate summary report
    print(f"\n{YELLOW}{'='*60}{NC}")
    print(f"{YELLOW}TEST SUMMARY REPORT{NC}")
    print(f"{YELLOW}{'='*60}{NC}")

    print(f"\nTotal Tests: {total_tests}")
    print(f"{GREEN}Passed: {passed_tests}{NC}")
    print(f"{RED}Failed: {failed_tests}{NC}")

    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    if success_rate == 100:
        print(f"\n{GREEN}🎉 ALL TESTS PASSED! ({success_rate:.1f}%){NC}")
        status = "PASS"
    elif success_rate >= 80:
        print(f"\n{YELLOW}⚠️  MOSTLY PASSING ({success_rate:.1f}%){NC}")
        status = "WARN"
    else:
        print(f"\n{RED}❌ TESTS FAILING ({success_rate:.1f}%){NC}")
        status = "FAIL"

    # Write detailed report
    report_path = Path("TEST_REPORT_2025-10-24.json")
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": success_rate,
            "status": status
        },
        "results": test_results,
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "working_dir": os.getcwd()
        }
    }

    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)

    print(f"\n📄 Detailed report saved to: {report_path}")

    return success_rate == 100

# Main execution
if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)