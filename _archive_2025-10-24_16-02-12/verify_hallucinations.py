#!/usr/bin/env python3
"""
Hallucination Verification Script

PURPOSE: Scan Acts 3-5 for claims and verify against source JSON data
DETECTS: Invented statistics, fabricated quotes, unverified claims

USAGE: python3 verify_hallucinations.py
OUTPUT: Detailed report of hallucinations found

AUTHOR: Claude Code
CREATED: 2025-10-23
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Any
from collections import defaultdict


class HallucinationDetector:
    """Detects fabricated content by comparing claims against source data"""

    def __init__(self, source_dir: Path, data_dir: Path):
        """
        Initialize detector

        Args:
            source_dir: Directory with markdown files (Acts 3-5)
            data_dir: Directory with JSON source data
        """
        self.source_dir = source_dir
        self.data_dir = data_dir
        self.all_json_content = {}
        self.findings = []

    def load_all_json_data(self):
        """Load all JSON files into memory for searching"""
        print("📦 Loading source JSON data...")

        json_files = list(self.data_dir.glob("*.json"))

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    self.all_json_content[json_file.name] = json.load(f)
                    print(f"   ✅ Loaded {json_file.name}")
            except Exception as e:
                print(f"   ⚠️  Failed to load {json_file.name}: {e}")

        print(f"\n📊 Loaded {len(self.all_json_content)} JSON files\n")

    def extract_numeric_claims(self, text: str) -> List[Tuple[str, int]]:
        """
        Extract numeric claims from text

        Returns:
            List of (claim_text, line_number) tuples
        """
        claims = []

        # Patterns to detect numeric claims
        patterns = [
            r'\d{1,3}(?:,\d{3})*\+?\s+(?:reviews|customers|interviews|tickets|queries|clients|employees)',
            r'\d+%\s+(?:increase|decrease|growth|of|more|less)',
            r'₹\d{1,3}(?:,\d{3})*(?:B|M|K)?',
            r'\$\d{1,3}(?:,\d{3})*(?:B|M|K)?',
            r'\d+(?:kg|g|L|ml)/(?:month|week|day|year)',
            r'Q[1-4]\s+FY\d{2}',
            r'Fortune\s+\d+',
        ]

        lines = text.split('\n')

        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    claims.append((match.group(), line_num, line.strip()))

        return claims

    def search_in_json(self, claim: str) -> List[str]:
        """
        Search for claim in all JSON data

        Returns:
            List of JSON filenames where claim was found
        """
        found_in = []

        # Normalize claim for searching (remove formatting)
        normalized_claim = claim.lower().replace(',', '')

        for filename, data in self.all_json_content.items():
            # Convert JSON to string for searching
            json_str = json.dumps(data, indent=2).lower()

            # Try exact match
            if normalized_claim in json_str:
                found_in.append(filename)
                continue

            # Try fuzzy match (just the number)
            numbers = re.findall(r'\d+', claim)
            if numbers:
                for num in numbers:
                    if num in json_str:
                        # Verify context is similar
                        # (to avoid false positives like "25" appearing in unrelated contexts)
                        claim_words = set(re.findall(r'\w+', claim.lower()))

                        # Extract context around the number in JSON
                        num_index = json_str.find(num)
                        context = json_str[max(0, num_index-50):num_index+50]
                        context_words = set(re.findall(r'\w+', context))

                        # Check if at least 1 keyword matches
                        if claim_words & context_words:
                            found_in.append(f"{filename} (fuzzy match)")
                            break

        return found_in

    def verify_act(self, act_file: Path, act_name: str):
        """Verify a single Act file"""
        print(f"🔍 Scanning {act_name}...")

        if not act_file.exists():
            print(f"   ⚠️  File not found: {act_file}")
            return

        # Read Act content
        with open(act_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract claims
        claims = self.extract_numeric_claims(content)

        print(f"   📊 Found {len(claims)} numeric claims")

        # Verify each claim
        hallucinations = []
        verified = []

        for claim, line_num, full_line in claims:
            sources = self.search_in_json(claim)

            if sources:
                verified.append({
                    'claim': claim,
                    'line': line_num,
                    'context': full_line,
                    'sources': sources
                })
            else:
                hallucinations.append({
                    'claim': claim,
                    'line': line_num,
                    'context': full_line
                })

        # Store findings
        self.findings.append({
            'act': act_name,
            'file': act_file.name,
            'total_claims': len(claims),
            'verified': verified,
            'hallucinations': hallucinations
        })

        print(f"   ✅ Verified: {len(verified)}")
        print(f"   ❌ Hallucinations: {len(hallucinations)}\n")

    def generate_report(self) -> str:
        """Generate detailed report"""
        report = []

        report.append("=" * 80)
        report.append("HALLUCINATION VERIFICATION REPORT")
        report.append("=" * 80)
        report.append("")

        total_claims = 0
        total_verified = 0
        total_hallucinations = 0

        for finding in self.findings:
            total_claims += finding['total_claims']
            total_verified += len(finding['verified'])
            total_hallucinations += len(finding['hallucinations'])

            report.append(f"\n## {finding['act']}")
            report.append(f"File: {finding['file']}")
            report.append(f"Total Claims: {finding['total_claims']}")
            report.append("")

            # Verified claims
            if finding['verified']:
                report.append("### ✅ VERIFIED CLAIMS")
                report.append("")
                for v in finding['verified'][:5]:  # Show first 5
                    report.append(f"Line {v['line']}: \"{v['claim']}\"")
                    report.append(f"  Found in: {', '.join(v['sources'])}")
                    report.append("")

                if len(finding['verified']) > 5:
                    report.append(f"  ... and {len(finding['verified']) - 5} more verified claims")
                    report.append("")

            # Hallucinations
            if finding['hallucinations']:
                report.append("### ❌ HALLUCINATIONS (Not Found in Source Data)")
                report.append("")
                for h in finding['hallucinations']:
                    report.append(f"Line {h['line']}: \"{h['claim']}\"")
                    report.append(f"  Context: {h['context'][:80]}...")
                    report.append("")

        # Summary
        report.append("\n" + "=" * 80)
        report.append("SUMMARY")
        report.append("=" * 80)
        report.append(f"Total Claims Found: {total_claims}")
        report.append(f"✅ Verified: {total_verified} ({total_verified/total_claims*100:.1f}%)")
        report.append(f"❌ Hallucinations: {total_hallucinations} ({total_hallucinations/total_claims*100:.1f}%)")
        report.append("")

        if total_hallucinations > 0:
            report.append("⚠️  ACTION REQUIRED:")
            report.append("   1. Remove hallucinated claims from markdown files")
            report.append("   2. Add real data to source JSON files")
            report.append("   3. Create data-driven generators for Acts 3-5")
        else:
            report.append("✅ ALL CLAIMS VERIFIED - No hallucinations detected!")

        return "\n".join(report)


def main():
    """Run verification"""
    print("🚀 Hallucination Verification Tool\n")

    # Paths
    base_dir = Path(__file__).parent
    source_dir = base_dir / "source"
    data_dir = Path("/Users/kalpeshjaju/Development/flyberry_oct_restart/extracted_data")

    # Initialize detector
    detector = HallucinationDetector(source_dir, data_dir)

    # Load all JSON data
    detector.load_all_json_data()

    # Verify Acts 3-5
    acts_to_verify = [
        (source_dir / "act-3-discoveries.md", "Act 3: What We Discovered"),
        (source_dir / "act-4-market-proof.md", "Act 4: Market Proof"),
        (source_dir / "act-5-where-to-go.md", "Act 5: Where We Should Go"),
    ]

    for act_file, act_name in acts_to_verify:
        detector.verify_act(act_file, act_name)

    # Generate report
    report = detector.generate_report()

    # Print to console
    print(report)

    # Save to file
    report_file = base_dir / "HALLUCINATION_REPORT.md"
    report_file.write_text(report, encoding='utf-8')
    print(f"\n📄 Report saved to: {report_file}")


if __name__ == "__main__":
    main()
