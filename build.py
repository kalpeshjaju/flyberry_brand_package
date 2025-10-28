#!/usr/bin/env python3
"""
Flyberry Brand Package Builder
Converts Markdown files to HTML using templates

DATA SOURCE: flyberry_oct_restart (INPUT folder)
All content MUST be generated from structured JSON - NO static markdown allowed.
"""

import markdown
import os
import sys
from pathlib import Path
from datetime import datetime
import re

# Import data integration (connects to INPUT folder)
from data_integration import get_data_source

# Import generators
from generators.act1_generator import generate_act1_markdown
from generators.act2_generator import generate_act2_markdown

# Configuration
SOURCE_DIR = Path("source")
TEMPLATE_DIR = Path("templates")
OUTPUT_DIR = Path("docs")
ASSETS_DIR = Path("assets")

# Act configuration
ACTS = [
    {
        "number": "1",
        "file": "act-1-who-we-are",
        "title": "WHO WE ARE",
        "subtitle": "Foundation & Heritage",
        "description": "Flyberry's origin story, sourcing philosophy, hero products, and brand promise"
    },
    {
        "number": "2",
        "file": "act-2-where-we-are",
        "title": "WHERE WE ARE TODAY",
        "subtitle": "Current State Assessment",
        "description": "Brutal brand audit, current performance, customers, and challenges"
    },
    {
        "number": "3",
        "file": "act-3-discoveries",
        "title": "WHAT WE DISCOVERED",
        "subtitle": "Insights & Opportunities",
        "description": "Customer research, market opportunities, and competitive analysis"
    },
    {
        "number": "4",
        "file": "act-4-market-proof",
        "title": "MARKET PROOF",
        "subtitle": "Validation Before Strategy",
        "description": "Evidence-based validation of assumptions and market readiness"
    },
    {
        "number": "5",
        "file": "act-5-where-to-go",
        "title": "WHERE WE SHOULD GO",
        "subtitle": "Strategy Based on Evidence",
        "description": "Brand vision, positioning strategy, and implementation roadmap"
    }
]


def read_template(template_name):
    """Read HTML template"""
    template_path = TEMPLATE_DIR / f"{template_name}.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def add_section_classes(html_content):
    """Add CSS classes to sections for styling flexibility"""
    # Split content by DOCUMENT headers to wrap each section
    # Match: <h2 id="...">DOCUMENT 00: Title</h2>
    doc_pattern = r'(<h2[^>]*>DOCUMENT (\d+):.*?</h2>)'

    parts = re.split(doc_pattern, html_content)

    if len(parts) > 1:
        result = parts[0]  # Content before first document

        # Process document sections
        i = 1
        while i < len(parts):
            if i + 2 < len(parts):
                doc_header = parts[i]  # Full <h2>DOCUMENT XX:...</h2>
                doc_number = parts[i + 1]  # Just the number
                doc_content = parts[i + 2]  # Content until next doc

                # Wrap in document-section div
                result += f'<div class="document-section doc-{doc_number}">'
                result += doc_header.replace('<h2', '<h2 class="doc-title"')
                result += doc_content
                result += '</div>'

                i += 3
            else:
                result += parts[i]
                i += 1

        html_content = result

    return html_content


def convert_markdown(md_content):
    """Convert markdown to HTML with section-specific classes"""
    md = markdown.Markdown(extensions=[
        'extra',           # Tables, fenced code blocks, etc.
        'nl2br',           # New line to <br>
        'sane_lists',      # Better list handling
        'toc',             # Table of contents
        'attr_list',       # Add attributes to elements
    ])
    html = md.convert(md_content)

    # Add section-specific CSS classes
    html = add_section_classes(html)

    return html


def simple_template_render(template, context):
    """Simple template variable replacement (no Jinja2 dependency)"""
    result = template

    # Replace simple variables
    for key, value in context.items():
        if value is None:
            value = ""
        result = result.replace(f"{{{{ {key} }}}}", str(value))

    # Handle conditionals - {% if prev_act %}
    if context.get('prev_act'):
        result = re.sub(r'{%\s*if\s+prev_act\s*%}(.*?){%\s*else\s*%}.*?{%\s*endif\s*%}',
                       r'\1', result, flags=re.DOTALL)
    else:
        result = re.sub(r'{%\s*if\s+prev_act\s*%}.*?{%\s*else\s*%}(.*?){%\s*endif\s*%}',
                       r'\1', result, flags=re.DOTALL)

    if context.get('next_act'):
        result = re.sub(r'{%\s*if\s+next_act\s*%}(.*?){%\s*else\s*%}.*?{%\s*endif\s*%}',
                       r'\1', result, flags=re.DOTALL)
    else:
        result = re.sub(r'{%\s*if\s+next_act\s*%}.*?{%\s*else\s*%}(.*?){%\s*endif\s*%}',
                       r'\1', result, flags=re.DOTALL)

    # Handle active class
    for i in range(1, 6):
        if context.get('act_number') == str(i):
            result = result.replace(f"{{% if act_number == '{i}' %}}active{{% endif %}}", "active")
        else:
            result = result.replace(f"{{% if act_number == '{i}' %}}active{{% endif %}}", "")

    return result


def generate_dynamic_acts(data_source):
    """
    Generate markdown files dynamically from structured data

    Args:
        data_source: BrandPackageDataSource instance
    """
    # Generate Act 1 from structured data
    print("  → Generating Act 1 from product catalog...")
    act1_md = generate_act1_markdown(data_source)

    # Write to source directory (overwrite static version)
    act1_file = SOURCE_DIR / "act-1-who-we-are.md"
    act1_file.write_text(act1_md, encoding='utf-8')
    print(f"  ✅ Act 1 generated ({len(act1_md)} chars)")

    # Generate Act 2 from Q1 FY26 data
    print("  → Generating Act 2 from Q1 FY26 financials...")
    act2_md = generate_act2_markdown()

    # Write Act 2 to source directory
    act2_file = SOURCE_DIR / "act-2-where-we-are.md"
    act2_file.write_text(act2_md, encoding='utf-8')
    print(f"  ✅ Act 2 generated ({len(act2_md)} chars)")

    # TODO: Add generators for Acts 3-5
    print("  ⏭️  Acts 3-5 using static markdown (will be migrated)")


def build_act(act_info, prev_act=None, next_act=None):
    """Build a single act HTML file"""
    md_file = SOURCE_DIR / f"{act_info['file']}.md"

    if not md_file.exists():
        print(f"⚠️  Markdown file not found: {md_file}")
        return False

    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert to HTML
    html_content = convert_markdown(md_content)

    # Read template
    template = read_template('act')

    # Check for custom CSS
    custom_css_file = ASSETS_DIR / "css" / f"{act_info['file']}-custom.css"
    custom_css = ""
    if custom_css_file.exists():
        custom_css = f'<link rel="stylesheet" href="assets/css/{act_info["file"]}-custom.css">'

    # Prepare context
    context = {
        'title': f"Act {act_info['number']}: {act_info['title']}",
        'description': act_info['description'],
        'act_number': act_info['number'],
        'act_title': act_info['title'],
        'act_subtitle': act_info['subtitle'],
        'act_file': act_info['file'],
        'content': html_content,
        'custom_css': custom_css,
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'prev_act.url': prev_act['file'] + '.html' if prev_act else None,
        'prev_act.title': prev_act['title'] if prev_act else None,
        'next_act.url': next_act['file'] + '.html' if next_act else None,
        'next_act.title': next_act['title'] if next_act else None,
        'prev_act': prev_act,
        'next_act': next_act,
    }

    # Render template
    html_output = simple_template_render(template, context)

    # Write output
    output_file = OUTPUT_DIR / f"{act_info['file']}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"✅ Built: {output_file.name}")
    return True


def generate_research_tasks(missing_data):
    """
    Generate RESEARCH_NEEDED.md with detailed tasks for missing data

    Args:
        missing_data: List of missing reference files with details
    """
    from datetime import datetime

    output = []
    output.append("# 📋 Research Tasks Required")
    output.append(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append(f"**Missing Files**: {len(missing_data)}")
    output.append("\n---\n")

    output.append("## Quick Summary\n")
    for item in missing_data:
        output.append(f"- [ ] {item['file']} ({item['act'].upper()})")
    output.append("\n---\n")

    # Group by act
    acts_data = {}
    for item in missing_data:
        act = item['act']
        if act not in acts_data:
            acts_data[act] = []
        acts_data[act].append(item)

    # Generate detailed tasks
    for act, items in sorted(acts_data.items()):
        output.append(f"## {act.upper()} Requirements\n")

        for item in items:
            output.append(f"### 📁 {item['file']}\n")
            output.append(f"**Purpose**: {item['description']}\n")
            output.append(f"**Impact**: {item['impact']}\n")
            output.append("\n**Suggested Data Sources**:")
            for source in item['sources']:
                output.append(f"- {source}")

            output.append("\n**Data Structure Template**:")
            output.append("```json")
            output.append("{")
            output.append('  "metadata": {')
            output.append('    "source": "[Source name/URL]",')
            output.append(f'    "date": "{datetime.now().strftime("%Y-%m-%d")}",')
            output.append('    "extractedBy": "[Your name/Claude/ChatGPT]",')
            output.append('    "confidence": "[high/medium/low]",')
            output.append('    "needsVerification": true/false')
            output.append('  },')
            output.append('  "data": {')
            output.append('    // Add structured data here')
            output.append('  }')
            output.append("}")
            output.append("```")

            output.append("\n**Collection Steps**:")
            output.append("1. Research from suggested sources")
            output.append("2. Save raw data to: `raw_data/references/`")
            output.append("3. Create markdown version: `llm_readable/*-reference.md`")
            output.append(f"4. Extract to JSON: `extracted_data/{item['file']}`")
            output.append("5. Update `data-lineage.json` with source tracking")
            output.append("\n---\n")

    # Add instructions
    output.append("## 📝 How to Complete These Tasks\n")
    output.append("### Step 1: Gather Data")
    output.append("- Use web search, official sources, or LLM assistance")
    output.append("- Save screenshots/PDFs as proof in `raw_data/references/`")
    output.append("")
    output.append("### Step 2: Process Data")
    output.append("```bash")
    output.append("# Example for competitor data")
    output.append("cd flyberry_oct_restart")
    output.append("")
    output.append("# 1. Save raw source")
    output.append("echo 'Source data...' > raw_data/references/competitors-web-2025-10.md")
    output.append("")
    output.append("# 2. Create readable version")
    output.append("cp raw_data/references/competitors-web-2025-10.md \\")
    output.append("   llm_readable/competitors-reference.md")
    output.append("")
    output.append("# 3. Extract to JSON")
    output.append("# Create extracted_data/competitors-reference.json with structure above")
    output.append("```")
    output.append("")
    output.append("### Step 3: Update Tracking")
    output.append("Add to `data-lineage.json`:")
    output.append("```json")
    output.append('"competitors-reference.json": {')
    output.append('  "sourceMarkdown": "llm_readable/competitors-reference.md",')
    output.append('  "sourceRaw": "raw_data/references/competitors-web-2025-10.md",')
    output.append('  "extractionMethod": "manual/llm-assisted",')
    output.append('  "confidence": "medium",')
    output.append('  "isReference": true')
    output.append("}")
    output.append("```")
    output.append("")
    output.append("### Step 4: Test")
    output.append("```bash")
    output.append("cd ../flyberry_brand_package")
    output.append("python3 build.py")
    output.append("# Should no longer show missing data warnings")
    output.append("```")
    output.append("\n---\n")
    output.append(f"*Generated by Flyberry Brand Package Builder*")

    # Write to file
    with open("RESEARCH_NEEDED.md", "w") as f:
        f.write("\n".join(output))


def build_all():
    """Build all acts"""
    print("🚀 Building Flyberry Brand Package...")
    print()

    # CRITICAL: Load structured data from INPUT folder
    print("📦 Loading structured data from INPUT folder...")
    data_source = get_data_source()
    print()

    # Check for missing reference data
    print("🔍 Checking data completeness...")
    missing_data = data_source.check_data_completeness()

    if missing_data:
        print("⚠️  Missing Reference Data Detected:")
        print("=" * 60)
        for item in missing_data:
            print(f"\n📍 {item['act'].upper()}: {item['file']}")
            print(f"   Description: {item['description']}")
            print(f"   Suggested sources: {', '.join(item['sources'][:3])}")

        print("\n" + "=" * 60)
        print("\n💡 Options:")
        print("1. Continue with gaps (some sections will be incomplete)")
        print("2. Generate research tasks and exit")
        print("3. Exit now")

        response = input("\nYour choice (1/2/3): ").strip()

        if response == '2':
            # Generate research tasks
            generate_research_tasks(missing_data)
            print("\n✅ Research tasks generated: RESEARCH_NEEDED.md")
            print("📋 Complete the research tasks, then run build again.")
            sys.exit(0)
        elif response == '3':
            print("\n🛑 Build cancelled.")
            sys.exit(0)
        else:
            print("\n⚠️  Continuing with gaps. Some sections may be incomplete.\n")
    else:
        print("✅ All reference data available!\n")

    # Generate dynamic content from structured data
    print("📝 Generating Acts from structured data...")
    generate_dynamic_acts(data_source)
    print()

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Copy assets if needed
    import shutil
    assets_dest = OUTPUT_DIR / "assets"
    if assets_dest.exists():
        shutil.rmtree(assets_dest)
    shutil.copytree(ASSETS_DIR, assets_dest)
    print("✅ Copied assets")
    print()

    # Build each act
    for i, act in enumerate(ACTS):
        prev_act = ACTS[i-1] if i > 0 else None
        next_act = ACTS[i+1] if i < len(ACTS) - 1 else None
        build_act(act, prev_act, next_act)

    print()
    print("🎉 Build complete!")
    print(f"📂 Output directory: {OUTPUT_DIR.absolute()}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        act_file = sys.argv[1]
        # Build specific act
        act_info = next((a for a in ACTS if a['file'] == act_file), None)
        if not act_info:
            print(f"❌ Unknown act: {act_file}")
            print(f"Available acts: {', '.join(a['file'] for a in ACTS)}")
            sys.exit(1)

        i = ACTS.index(act_info)
        prev_act = ACTS[i-1] if i > 0 else None
        next_act = ACTS[i+1] if i < len(ACTS) - 1 else None
        build_act(act_info, prev_act, next_act)
    else:
        # Build all
        build_all()


if __name__ == "__main__":
    main()
