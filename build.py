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

    # TODO: Add generators for Acts 2-5
    print("  ⏭️  Acts 2-5 using static markdown (will be migrated)")


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


def build_all():
    """Build all acts"""
    print("🚀 Building Flyberry Brand Package...")
    print()

    # CRITICAL: Load structured data from INPUT folder
    print("📦 Loading structured data from INPUT folder...")
    data_source = get_data_source()
    print()

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
