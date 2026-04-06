#!/usr/bin/env python3
"""
Preview the HTML that main.py generates from sources.md at server startup.

Useful for checking your edits to sources.md before restarting the server.
The actual parsing lives in breathe_fastapi/main.py (_parse_sources_md).

Usage:
  python utilities/generate_sources.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SOURCES_MD = ROOT / "sources.md"


# ---------------------------------------------------------------------------
# Parsing  (keep in sync with _parse_sources_md in main.py)
# ---------------------------------------------------------------------------


def parse_sources_md(text: str) -> dict:
    """
    Parse sources.md into a nested dict.

    Structure:
      # Category              <- tier 1
      ## function_name        <- tier 2 (may be "Additional")
      ### Sources/Steps/Notes <- tier 3
    """
    parsed: dict = {}
    current_category: str | None = None
    current_func: str | None = None
    current_subsec: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if re.match(r"^# [^#]", line):
            current_category = line[2:].strip()
            parsed[current_category] = {}
            current_func = None
            current_subsec = None
        elif re.match(r"^## [^#]", line):
            current_func = line[3:].strip()
            if current_category is not None:
                parsed[current_category][current_func] = {
                    "sources": [],
                    "steps": [],
                    "notes": [],
                }
            current_subsec = None
        elif re.match(r"^### [^#]", line):
            label = line[4:].strip().rstrip(":").lower()
            current_subsec = label if label in ("sources", "steps", "notes") else None
        elif current_category and current_func and current_subsec:
            bucket = parsed[current_category][current_func][current_subsec]
            if line.startswith("* ") or line.startswith("- "):
                bucket.append(line[2:].strip())
            elif re.match(r"^\d+\. ", line):
                bucket.append(re.sub(r"^\d+\. ", "", line).strip())
            elif line:
                bucket.append(line)

    return parsed


# ---------------------------------------------------------------------------
# Markdown helpers  (keep in sync with _inline_md in main.py)
# ---------------------------------------------------------------------------


def _inline_md(text: str) -> str:
    # Markdown links — handle URLs containing one level of parentheses
    text = re.sub(
        r"\[([^\]]+)\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)",
        r'<a href="\2" target="_blank">\1</a>',
        text,
    )
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Auto-link bare URLs, stripping trailing punctuation
    text = re.sub(
        r'(?<!href=")(https?://[^\s<>"]+?)([.,;:)]*)(?=\s|$)',
        lambda m: f'<a href="{m.group(1)}" target="_blank">{m.group(1)}</a>{m.group(2)}',
        text,
    )
    return text


# ---------------------------------------------------------------------------
# Display name map  (keep in sync with _FUNC_DISPLAY in main.py)
# ---------------------------------------------------------------------------

_FUNC_DISPLAY: dict[str, str] = {
    "make_economy_income": "Income",
    "make_economy_barchart": "Income Bar Chart",
    "make_economy_house_purchase": "Housing Costs",
    "make_economy_f150": "Ford F-150 Price",
    "make_economy_income_taxes": "Income Taxes",
    "make_american_dream_kids": "American Dream - Kids",
    "make_mobility_international": "Mobility - International",
    "make_county_heatmap": "Upward Mobility",
    "make_healthcare": "Healthcare",
    "make_justice_jail": "Justice - Incarceration",
    "make_electricity_cost": "Electricity Cost",
    "make_state_home_affordability": "State Home Affordability",
    "Additional": "Additional Sources",
}


def _func_display(category: str, func_name: str) -> str:
    if func_name in _FUNC_DISPLAY:
        return _FUNC_DISPLAY[func_name]
    name = func_name.removeprefix("make_")
    cat_prefix = category.lower().replace(" ", "_") + "_"
    if name.startswith(cat_prefix):
        name = name[len(cat_prefix) :]
    return name.replace("_", " ").title() or category


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------


def generate_page_html(parsed: dict) -> str:
    lines = [
        "<h1>Sources</h1>",
        '<p class="sources-intro">The data used for the Breathe Voter Compass '
        "comes from publicly available sources listed below.</p>",
        "",
    ]
    for category, funcs in parsed.items():
        for func_name, data in funcs.items():
            sources, steps, notes = data["sources"], data["steps"], data["notes"]
            if not sources and not steps and not notes:
                continue
            display = _func_display(category, func_name)
            if func_name == "Additional":
                title = f"{category} - Additional Sources"
            else:
                title = (
                    display
                    if display.lower().startswith(category.lower())
                    else f"{category} - {display}"
                )
            lines.append("  <section>")
            lines.append(f"    <h2>{title}</h2>")
            for note in notes:
                lines.append(f"    <p>{_inline_md(note)}</p>")
            if sources:
                lines.append("    <ul>")
                lines += [f"      <li>{_inline_md(s)}</li>" for s in sources]
                lines.append("    </ul>")
            if steps:
                lines.append("    <ol>")
                lines += [f"      <li>{_inline_md(s)}</li>" for s in steps]
                lines.append("    </ol>")
            lines.append("  </section>")
            lines.append("")
    return "\n".join(lines)


def generate_popup_data(parsed: dict) -> dict[str, str]:
    result: dict[str, str] = {}
    for _cat, funcs in parsed.items():
        for func_name, data in funcs.items():
            if func_name == "Additional":
                continue
            sources, steps = data["sources"], data["steps"]
            if not sources and not steps:
                continue
            parts: list[str] = []
            if sources:
                parts += ["<p><strong>Sources</strong></p>", "<ul>"]
                parts += [f"  <li>{_inline_md(s)}</li>" for s in sources]
                parts.append("</ul>")
            if steps:
                parts += ["<p><strong>Steps</strong></p>", "<ol>"]
                parts += [f"  <li>{_inline_md(s)}</li>" for s in steps]
                parts.append("</ol>")
            result[func_name] = "\n".join(parts)
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    if not SOURCES_MD.exists():
        sys.exit(f"ERROR: {SOURCES_MD} not found")

    parsed = parse_sources_md(SOURCES_MD.read_text(encoding="utf-8"))

    sep = "-" * 72
    print(sep)
    print("OUTPUT 1: Sources tab page HTML (served via /api/sources -> data.page)")
    print(sep)
    print(generate_page_html(parsed))
    print()

    print(sep)
    print("OUTPUT 2: Per-chart popup HTML (served via /api/sources -> data.popup)")
    print(sep)
    print(json.dumps(generate_popup_data(parsed), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
