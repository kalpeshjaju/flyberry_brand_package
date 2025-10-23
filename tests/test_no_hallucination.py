#!/usr/bin/env python3
"""
Anti-Hallucination Test Suite

PURPOSE: Prevent hard-coded/fabricated data in generators
RUNS: pytest tests/test_no_hallucination.py

This test ensures generators ONLY read from JSON files and
do NOT contain hard-coded dictionaries, fabricated stories,
invented statistics, or fake corporate details.

AUTHOR: Claude Code
CREATED: 2025-10-23
"""

import os
from pathlib import Path
import re


def test_no_hardcoded_dictionaries():
    """
    Ensure generators don't contain hard-coded data dictionaries

    FORBIDDEN PATTERNS:
    - origin_stories = {...}
    - use_cases = {...}
    - client_stories = [...]
    - nut_origin_stories = {...}
    - Any large hard-coded data structures
    """
    generator_files = [
        'generators/document_builders_01_02.py',
        'generators/document_builders_03_04.py',
        'generators/document_builders_05_06.py',
        'generators/act1_generator.py'
    ]

    # Forbidden patterns that indicate hallucination
    forbidden_patterns = [
        r'origin_stories\s*=\s*\{',
        r'nut_origin_stories\s*=\s*\{',
        r'use_cases\s*=\s*\{',
        r'client_stories\s*=\s*\[',
        r'case_studies\s*=\s*\[',
        r'terroir_info\s*=\s*\{',
        r'competitive_comparisons\s*=\s*\{',
        r'industry_stats\s*=\s*\{',
    ]

    for gen_file in generator_files:
        if not os.path.exists(gen_file):
            continue

        with open(gen_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # STEP: Filter out docstrings and comments
        # WHY: Warning comments contain pattern examples, we only want to detect actual code
        code_lines = []
        in_docstring = False
        for line in lines:
            # Skip docstrings
            if '"""' in line or "'''" in line:
                in_docstring = not in_docstring
                continue
            if in_docstring:
                continue
            # Skip comment-only lines
            if line.strip().startswith('#'):
                continue
            code_lines.append(line)

        content = ''.join(code_lines)

        for pattern in forbidden_patterns:
            # Add ^ to match only at start of line (actual code, not in strings)
            pattern_with_anchor = r'^' + pattern.lstrip('^')
            match = re.search(pattern_with_anchor, content, re.MULTILINE)
            assert not match, (
                f"❌ HALLUCINATION DETECTED in {gen_file}:\n"
                f"   Found forbidden pattern: {pattern}\n"
                f"   Line: {content[:match.start()].count(chr(10)) + 1}\n"
                f"   \n"
                f"   RULE: Generators must ONLY read from JSON files.\n"
                f"   FIX: Move this data to a JSON file in extracted_data/"
            )


def test_no_suspicious_long_strings():
    """
    Flag suspiciously long string literals that might be fabricated content

    RULE: Generators should have SHORT template strings only.
    Long strings (>500 chars) are suspicious and likely fabricated.
    """
    generator_files = [
        'generators/document_builders_01_02.py',
        'generators/document_builders_03_04.py',
        'generators/document_builders_05_06.py',
    ]

    for gen_file in generator_files:
        if not os.path.exists(gen_file):
            continue

        with open(gen_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all string literals
        # Match both single and triple-quoted strings
        pattern = r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"]*"|\'[^\']*\''
        strings = re.findall(pattern, content)

        for string_literal in strings:
            # Skip docstrings (they're long and that's OK)
            if string_literal.startswith('"""') or string_literal.startswith("'''"):
                continue

            # Skip markdown template strings (they're long but structural, not data)
            if '##' in string_literal or '**' in string_literal:
                continue

            # Flag very long strings (likely fabricated data)
            if len(string_literal) > 500:
                assert False, (
                    f"❌ SUSPICIOUS LONG STRING in {gen_file}:\n"
                    f"   Length: {len(string_literal)} chars (limit: 500)\n"
                    f"   Preview: {string_literal[:100]}...\n"
                    f"   \n"
                    f"   LIKELY: Fabricated content hard-coded in generator\n"
                    f"   FIX: Move this content to JSON file or shorten template"
                )


def test_generators_read_json_files():
    """
    Verify generators actually read from JSON files

    RULE: Every generator must load data from JSON files.
    If not reading JSON, where is data coming from?
    """
    generator_files = [
        'generators/document_builders_01_02.py',
        'generators/document_builders_03_04.py',
        'generators/document_builders_05_06.py',
    ]

    for gen_file in generator_files:
        if not os.path.exists(gen_file):
            continue

        with open(gen_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Should have data_source parameter usage
        has_data_source = 'data_source' in content

        # Or should read JSON files directly
        has_json_load = 'json.load' in content or '.get_' in content

        assert has_data_source or has_json_load, (
            f"❌ NO DATA SOURCE in {gen_file}:\n"
            f"   Generators must read from data_source or load JSON files.\n"
            f"   If no data loading found, where is content coming from?\n"
            f"   \n"
            f"   FIX: Ensure generator uses data_source parameter or json.load()"
        )


def test_no_invented_corporate_details():
    """
    Ensure corporate client details are not fabricated

    RULE: Corporate data must come from corporate-clients.json ONLY.
    Do NOT invent volumes, case studies, audit results, etc.
    """
    gen_file = 'generators/document_builders_05_06.py'

    if not os.path.exists(gen_file):
        return

    with open(gen_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # STEP: Filter out docstrings and comments (same as test_no_hardcoded_dictionaries)
    # WHY: Warning comments contain example phrases, we only want to detect actual code
    code_lines = []
    in_docstring = False
    for line in lines:
        if '"""' in line or "'''" in line:
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        if line.strip().startswith('#'):
            continue
        code_lines.append(line)

    content = ''.join(code_lines)

    # Suspicious phrases that indicate fabricated corporate details
    suspicious_phrases = [
        '500kg/month',
        '5,000+ employees',
        '8 offices',
        'blind taste test',
        'beat Bateel',
        'passed audit',
        'Google Food Safety audit',
    ]

    for phrase in suspicious_phrases:
        assert phrase not in content, (
            f"❌ FABRICATED CORPORATE DETAIL in {gen_file}:\n"
            f"   Found: '{phrase}'\n"
            f"   \n"
            f"   RULE: Corporate details must come from corporate-clients.json\n"
            f"   FOUND IN JSON: Client name, sector, use case, testimonial\n"
            f"   NOT IN JSON: Specific volumes, audit details, case studies\n"
            f"   \n"
            f"   FIX: Use ONLY what's in corporate-clients.json or add to JSON first"
        )


if __name__ == '__main__':
    """Run tests directly"""
    print("🔍 Running Anti-Hallucination Tests...\n")

    try:
        test_no_hardcoded_dictionaries()
        print("✅ PASS: No hard-coded dictionaries")
    except AssertionError as e:
        print(f"❌ FAIL: {e}\n")
        exit(1)

    try:
        test_no_suspicious_long_strings()
        print("✅ PASS: No suspicious long strings")
    except AssertionError as e:
        print(f"❌ FAIL: {e}\n")
        exit(1)

    try:
        test_generators_read_json_files()
        print("✅ PASS: Generators read from JSON")
    except AssertionError as e:
        print(f"❌ FAIL: {e}\n")
        exit(1)

    try:
        test_no_invented_corporate_details()
        print("✅ PASS: No invented corporate details")
    except AssertionError as e:
        print(f"❌ FAIL: {e}\n")
        exit(1)

    print("\n🎉 ALL ANTI-HALLUCINATION TESTS PASSED")
    print("✅ Generators are clean - no fabricated data detected")
