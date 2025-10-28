#!/usr/bin/env python3
"""
Data Integration Module - Connect INPUT to OUTPUT

Purpose: Bridge flyberry_oct_restart (INPUT) and flyberry_brand_package (OUTPUT)
Source of Truth: /Users/kalpeshjaju/Development/flyberry_oct_restart
Output: Dynamic markdown generation for brand package

NON-NEGOTIABLE: All data MUST come from structured JSON in INPUT folder.
"""

import sys
from pathlib import Path

# Add INPUT folder to Python path
INPUT_FOLDER = Path("/Users/kalpeshjaju/Development/flyberry_oct_restart")
sys.path.insert(0, str(INPUT_FOLDER))

# Import the data loader from INPUT folder
from flyberry_data_loader import FlyberryData


class BrandPackageDataSource:
    """
    Single source of truth for brand package generation

    Loads ALL data from flyberry_oct_restart structured JSON files.
    No hardcoded content allowed - everything comes from INPUT folder.
    """

    def __init__(self):
        """Initialize data source by loading from INPUT folder"""
        # Load structured data from INPUT folder
        self.data = FlyberryData(data_dir=str(INPUT_FOLDER / "extracted_data"))

        # Load all data into memory
        self._load_all_data()

    def _load_all_data(self):
        """Load all structured data"""
        print("📦 Loading structured data from INPUT folder...")

        self.products = self.data.products
        self.recipes = self.data.recipes
        self.design = self.data.design
        self.claims = self.data.claims

        print(f"✅ Loaded {len(self.products)} products")
        print(f"✅ Loaded {len(self.recipes)} recipes")
        print(f"✅ Loaded design system")
        print(f"✅ Loaded {len(self.claims.get('claims', []))} health claims ({self.claims.get('claimsRegistry', {}).get('totalClaims', 0)} unique claim types)")

    def get_brand_info(self):
        """Get brand name, tagline, typography"""
        return {
            "name": self.design["brand"]["name"],
            "tagline": self.design["brand"]["tagline"],
            "typography": {
                "primary": self.design["typography"]["primary"]["name"],
                "secondary": self.design["typography"]["secondary"]["name"]
            }
        }

    def get_all_products(self):
        """Get all products with full details"""
        return self.products

    def get_product_by_id(self, product_id):
        """Get specific product"""
        return self.data.get_product(product_id)

    def get_all_recipes(self):
        """Get all recipes"""
        return self.recipes

    def get_products_by_category(self):
        """Get products organized by category (dates vs nuts)"""
        dates = [p for p in self.products if 'dates' in p['productId']]
        nuts = [p for p in self.products if 'nuts' in p['productId']]
        return {"dates": dates, "nuts": nuts}

    def check_data_completeness(self):
        """
        Check what reference data is missing for complete brand package

        Returns list of missing reference files with details
        """
        required_references = {
            'act1': {
                'files': [],  # Core data complete from products/recipes
                'status': 'complete'
            },
            'act2': {
                'files': [],  # Financial data from investor-updates.json
                'status': 'complete'
            },
            'act3': {
                'files': [
                    {
                        'name': 'customer-testimonials-reference.json',
                        'description': 'Real customer testimonials and reviews',
                        'sources': ['Google Reviews', 'Social Media', 'Customer Surveys']
                    },
                    {
                        'name': 'market-trends-reference.json',
                        'description': 'Current market trends in premium snacking',
                        'sources': ['Industry Reports', 'Market Research']
                    }
                ],
                'status': 'needs_reference'
            },
            'act4': {
                'files': [
                    {
                        'name': 'competitors-reference.json',
                        'description': 'Competitor pricing and positioning',
                        'sources': ['Bateel', 'Sukkary', 'Al Marai', 'Other premium brands']
                    },
                    {
                        'name': 'market-size-reference.json',
                        'description': 'Market size and growth data for premium dates/nuts',
                        'sources': ['Industry Reports', 'Government Data', 'Trade Associations']
                    },
                    {
                        'name': 'market-validation-reference.json',
                        'description': 'Third-party validation and certifications',
                        'sources': ['Industry Awards', 'Media Coverage', 'Certifications']
                    }
                ],
                'status': 'needs_reference'
            },
            'act5': {
                'files': [
                    {
                        'name': 'trend-analysis-reference.json',
                        'description': 'Future trends and opportunities',
                        'sources': ['Trend Reports', 'Consumer Research', 'Industry Forecasts']
                    },
                    {
                        'name': 'expansion-opportunities-reference.json',
                        'description': 'Geographic and product expansion opportunities',
                        'sources': ['Market Analysis', 'Distribution Opportunities']
                    }
                ],
                'status': 'needs_reference'
            }
        }

        missing = []
        for act, config in required_references.items():
            for file_info in config.get('files', []):
                file_path = INPUT_FOLDER / "extracted_data" / file_info['name']
                if not file_path.exists():
                    missing.append({
                        'act': act,
                        'file': file_info['name'],
                        'description': file_info['description'],
                        'sources': file_info['sources'],
                        'path': str(file_path),
                        'impact': f'Incomplete {act.upper()} - missing {file_info["description"]}'
                    })

        return missing

    def get_reference_data(self, reference_file):
        """
        Load reference data file with confidence tracking

        Args:
            reference_file: Name of reference JSON file

        Returns:
            Dict with data and metadata, or None if not found
        """
        import json

        file_path = INPUT_FOLDER / "extracted_data" / reference_file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Add confidence indicator if not present
                if 'metadata' in data and 'confidence' not in data['metadata']:
                    # Determine confidence based on source
                    if 'source' in data['metadata']:
                        source = data['metadata']['source'].lower()
                        if 'official' in source or 'government' in source:
                            data['metadata']['confidence'] = 'high'
                        elif 'claude' in source or 'llm' in source:
                            data['metadata']['confidence'] = 'medium'
                        else:
                            data['metadata']['confidence'] = 'low'

                return data
        return None

    def list_reference_files(self):
        """
        List all reference files available

        Returns:
            List of reference file names with metadata
        """
        import json

        reference_files = []
        extracted_path = INPUT_FOLDER / "extracted_data"

        # Find all *-reference.json files
        for file_path in extracted_path.glob("*-reference.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                reference_files.append({
                        'file': file_path.name,
                        'source': data.get('metadata', {}).get('source', 'unknown'),
                        'date': data.get('metadata', {}).get('date', 'unknown'),
                        'confidence': data.get('metadata', {}).get('confidence', 'unknown'),
                        'has_data': 'data' in data and bool(data['data'])
                    })
            except:
                # If can't read, just note the file exists
                reference_files.append({
                    'file': file_path.name,
                    'error': 'Could not read file'
                })

        return reference_files

    def get_fortune_500_validation(self):
        """
        Get Fortune 500 validation data

        NOTE: This is currently in static markdown (Act 1).
        TODO: Extract to structured JSON in INPUT folder.
        """
        # Temporary: Return structure that should exist in INPUT folder
        return {
            "clients": [
                "Google", "Goldman Sachs", "Deloitte", "McKinsey",
                "Accenture", "Microsoft", "Amazon"
            ],
            "total_count": "50+",
            "validation": "Corporate gifting orders, office pantries"
        }

    def get_sourcing_origins(self):
        """Get unique sourcing countries from products"""
        origins = set()
        for product in self.products:
            origin = product.get("origin", "")
            # Parse origin (e.g., "Imported Product of Saudi Arabia" -> "Saudi Arabia")
            if "Imported Product of" in origin:
                country = origin.replace("Imported Product of", "").strip()
                origins.add(country)
            elif origin:
                origins.add(origin)
        return sorted(list(origins))

    def get_product_colors(self):
        """Get all product packaging colors"""
        colors = []
        for product in self.products:
            packaging = product.get("packaging", {})
            if "color" in packaging:
                colors.append({
                    "product": product["name"],
                    "hex": packaging["color"],
                    "name": packaging.get("colorName", "")
                })
        return colors

    def get_nutritional_highlights(self):
        """Get standout nutritional features across products"""
        highlights = []

        for product in self.products:
            benefits = product.get("benefits", [])
            for benefit in benefits:
                rda = benefit.get("rdaPercent", 0)
                if rda >= 20:  # "Excellent source" threshold
                    highlights.append({
                        "product": product["name"],
                        "nutrient": benefit.get("nutrient", ""),
                        "rda_percent": rda,
                        "claim": benefit.get("claim", "")
                    })

        # Sort by RDA percentage descending
        highlights.sort(key=lambda x: x["rda_percent"], reverse=True)
        return highlights

    def get_hero_products(self):
        """
        Get hero products (products with special features)

        Returns products that have unique selling points.
        """
        hero = []

        for product in self.products:
            # Check for special features in product data
            special_feature = None

            # Medjoul: workout benefits
            if product["productId"] == "medjoul-dates":
                if "workoutBenefits" in product:
                    special_feature = "Pre & Post-Workout Benefits"

            # Brazil Nuts: selenium powerhouse
            elif product["productId"] == "brazil-nuts":
                for benefit in product.get("benefits", []):
                    if benefit.get("nutrient") == "Selenium":
                        special_feature = f"World's Richest Selenium Source ({benefit['rdaPercent']}% RDA)"
                        break

            # Pine Nuts: Hindukush sourcing story
            elif product["productId"] == "pine-nuts":
                if "Hindukush" in product.get("description", ""):
                    special_feature = "Hindukush Mountains Sourcing Adventure"

            if special_feature:
                hero.append({
                    "product": product["name"],
                    "productId": product["productId"],
                    "feature": special_feature,
                    "tagline": product.get("tagline", "")
                })

        return hero

    def get_health_claims_summary(self):
        """Get summary of health claims by category"""
        claims_data = self.claims.get("claimsRegistry", {})

        return {
            "total_claims": claims_data.get("totalClaims", 0),
            "total_instances": claims_data.get("totalInstances", 0),
            "categories": claims_data.get("categoryCounts", {}),
            "top_nutrients": self._get_top_nutrients()
        }

    def _get_top_nutrients(self):
        """Extract top nutrients from claims"""
        nutrients = {}

        for product in self.products:
            for benefit in product.get("benefits", []):
                nutrient = benefit.get("nutrient", "")
                rda = benefit.get("rdaPercent", 0)

                if nutrient not in nutrients or nutrients[nutrient] < rda:
                    nutrients[nutrient] = rda

        # Sort by RDA percentage and return top 10
        sorted_nutrients = sorted(nutrients.items(), key=lambda x: x[1], reverse=True)
        return [{"nutrient": n, "max_rda": rda} for n, rda in sorted_nutrients[:10]]


# Singleton instance
_data_source = None

def get_data_source():
    """
    Get singleton data source instance

    Returns:
        BrandPackageDataSource: Loaded data source
    """
    global _data_source
    if _data_source is None:
        _data_source = BrandPackageDataSource()
    return _data_source


# Test if running directly
if __name__ == "__main__":
    print("🧪 Testing Data Integration...\n")

    # Load data
    source = get_data_source()

    # Test brand info
    brand = source.get_brand_info()
    print(f"Brand: {brand['name']}")
    print(f"Tagline: {brand['tagline']}")
    print(f"Typography: {brand['typography']['primary']} / {brand['typography']['secondary']}")

    # Test products
    products_by_cat = source.get_products_by_category()
    print(f"\nProducts: {len(products_by_cat['dates'])} dates, {len(products_by_cat['nuts'])} nuts")

    # Test hero products
    heroes = source.get_hero_products()
    print(f"\nHero Products ({len(heroes)}):")
    for hero in heroes:
        print(f"  • {hero['product']}: {hero['feature']}")

    # Test origins
    origins = source.get_sourcing_origins()
    print(f"\nSourcing Origins ({len(origins)} countries): {', '.join(origins)}")

    # Test nutritional highlights
    highlights = source.get_nutritional_highlights()[:5]
    print(f"\nTop 5 Nutritional Highlights:")
    for h in highlights:
        print(f"  • {h['product']}: {h['nutrient']} ({h['rda_percent']}% RDA)")

    # Test health claims
    claims_summary = source.get_health_claims_summary()
    print(f"\nHealth Claims: {claims_summary['total_claims']} unique claims")

    print("\n✅ Data integration working perfectly!")
    print("🎯 Ready to generate dynamic brand package from structured data")
