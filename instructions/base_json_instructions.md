Mississauga Budget — PDF→JSON Extraction Plan (for Cursor)
Objective

Build a clean, extensible dataset from the split PDFs in data/splits/ using our canonical, drill-down JSON schema:

{
  "name": "City of Mississauga",
  "type": "root",
  "fiscal_year": 2025,
  "children": [
    {
      "name": "Information Technology",
      "type": "department",
      "children": [
        {
          "name": "Operating",
          "type": "dataset",
          "children": [
            {
              "name": "Labour",
              "type": "category",
              "children": [
                { "name": "2023", "type": "year", "amount": 25809 },
                { "name": "2024", "type": "year", "amount": 27087 },
                { "name": "2025", "type": "year", "amount": 27638 }
              ]
            }
          ]
        }
      ]
    }
  ]
}


We will:

Build citywide base JSONs from pages 205, 206, 207 (for 2025, 2026, 2027).

Walk remaining pages in ascending order; when a page is a department “Operating Budget Overview ($000s)”, create a per-department JSON drill-down file.

Folder layout (assumed)
project/
  data/
    splits/
      page_001.pdf
      ...
      page_205.pdf   ← citywide 2025 base
      page_206.pdf   ← citywide 2026 base
      page_207.pdf   ← citywide 2027 base
      page_224.pdf   ← example dept drilldown (Facilities & Property Mgmt)
      page_229.pdf   ← example dept drilldown (Fire & Emergency Services)
      ...
    base/            ← Cursor will write base_YYYY.json here
    departments/     ← Cursor will write one JSON per department here
    combined/        ← optional: Cursor may also write merged tree here


Create the missing folders if they don’t exist.

Parsing rules (apply everywhere)

Treat numbers as integers in thousands of dollars.

Strip commas and $.

Parentheses mean negative (e.g., (1,055) → -1055).

Ignore totals, subtotals, notes, revenue blocks, and percent columns.

Normalize whitespace; preserve official display names (department and category).

Years expected in department tables: 2023, 2024, 2025 (use 0 if a year is blank).

JSON must be valid UTF-8 and indented.

Phase 1 — Build citywide base JSONs (pages 205, 206, 207)

Inputs

data/splits/page_205.pdf → 2025 citywide summary

data/splits/page_206.pdf → 2026 citywide summary

data/splits/page_207.pdf → 2027 citywide summary

What to extract (each page):

A table listing Service Areas / Departments with their Proposed Operating Budget for that page’s year.

The “Proposed” column is the value to capture.

Ignore column headers like “Maintain Current Service Levels”, “New Initiatives”, and the trailing “Change from Prior Year (%)”.

Stop at or ignore any “Total …” lines.

Output files

data/base/base_2025.json

data/base/base_2026.json

data/base/base_2027.json

File content
For each year YYYY, write:

{
  "name": "City of Mississauga",
  "type": "root",
  "fiscal_year": YYYY,
  "children": [
    { "name": "<Department A>", "type": "department", "amount": <proposed_amount_integer>, "children": [] },
    { "name": "<Department B>", "type": "department", "amount": <proposed_amount_integer>, "children": [] }
  ]
}


Department rows to include: every service area listed in the citywide table (e.g., Corporate Transactions, Facilities & Property Management, Fire & Emergency Services, General Government, Information Technology, Mayor & Members of Council, Mississauga Library, Parks/Forestry/Environment, Planning & Building, Recreation & Culture, Regulatory Services, Roads, Transit).

Validation

JSON parses.

Each department appears once.

Amounts are integers.

fiscal_year matches the page: 2025 for 205, 2026 for 206, 2027 for 207.

Phase 2 — Department drill-downs (pages after the base pages)

Input scope

Iterate all remaining data/splits/page_*.pdf in ascending numeric order, starting after 207.

A page is a target if it clearly presents a department header and an “Operating Budget Overview ($000s)” table for that department.

Detect department header

Use the prominent page header text (e.g., “Facilities & Property Management”, “Fire & Emergency Services”, “Information Technology”, etc.).

Normalize spacing; keep the official case.

Extract the Operating Overview table

Columns: Description | 2023 Actuals | 2024 Adopted | 2025 Proposed.

For each expense category row (e.g., Labour, Equipment & Maintenance, Staff Development, etc.), capture the three year amounts.

Exclude:

“Total Expenses”

Revenue lines (Fees & Service Charges, Rents & Concessions, Transit Fares, Grants, Gas Tax, etc.)

Transfers that are clearly totals/roll-ups at the end of revenue blocks

If a value is blank, store 0.

Output file (one per department)

Location: data/departments/

Filename: <nn>_<slug>.json where <nn> is a two-digit sequence in discovery order (e.g., 01_facilities_and_property_management.json, 02_fire_and_emergency_services.json, 03_information_technology.json).

Content (hierarchical drill-down):

{
  "name": "<Department Name>",
  "type": "department",
  "children": [
    {
      "name": "Operating",
      "type": "dataset",
      "children": [
        {
          "name": "<Category>",
          "type": "category",
          "children": [
            { "name": "2023", "type": "year", "amount": <int> },
            { "name": "2024", "type": "year", "amount": <int> },
            { "name": "2025", "type": "year", "amount": <int> }
          ]
        }
      ]
    }
  ]
}


Validation for each department file

Valid JSON.

Top-level "type" is "department".

Contains exactly one "Operating" dataset node.

Each category has 2023/2024/2025 children with integer amount.

No totals or revenue lines included.

Optional — Combine for visualization (single file)

If needed, Cursor may also build a combined, visualization-ready tree from the 2025 base and the per-department drill-downs:

Input

data/base/base_2025.json

All data/departments/*.json

Output

data/combined/budget_2025_tree.json with:

{
  "name": "City of Mississauga",
  "type": "root",
  "fiscal_year": 2025,
  "children": [
    // each department from base_2025, enriched by its drill-down file if present
  ]
}


Merge rule

Start from base_2025.json children list (preserves order and amounts).

For each department, if a matching data/departments/<…>.json exists:

Replace the empty children array with the department’s "children" (the "Operating" dataset and categories).

Preserve the department’s amount field from the base file as-is.

Completion checks

data/base/base_2025.json, base_2026.json, base_2027.json exist and are valid.

data/departments/*.json exist for all departments that have Operating Overview pages processed.

(If combined) data/combined/budget_2025_tree.json exists and is valid, with enriched children for departments that have drill-downs.

Notes for ambiguous pages

If a page shows only revenues or non-Operating content, skip it for department drill-downs.

If two consecutive pages belong to the same department’s Operating Overview, merge their rows into the same department JSON file.

If a department appears in the citywide base but its Operating Overview page isn’t found yet, leave its children: [] in the combined file.