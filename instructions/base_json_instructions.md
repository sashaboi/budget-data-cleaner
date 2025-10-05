🧾 instructions.md (drop in project root)
# 🧩 Budget Data Extraction Instructions

## Goal
Extract structured budget data from PDF pages (starting with `data/splits/page_204.pdf`)  
and populate a canonical hierarchical JSON for Mississauga's 2025 budget visualization.

---

## Phase 1: Base JSON generation (City-Wide Overview)

### Input
`data/splits/page_204.pdf`

This page contains the **"General Government – Operating Overview ($000s)"** or **"City-Wide Summary"** table.  
It includes a table with columns similar to:

| Description | 2023 Actuals | 2024 Adopted Budget | 2025 Proposed Budget |
|--------------|--------------|---------------------|----------------------|
| Labour | 57,313 | 64,171 | 67,121 |
| Staff Development | 650 | 741 | 818 |
| ... | ... | ... | ... |

---

### Output format
Generate a single JSON file at:


data/budget_2025_tree.json


**Canonical schema:**

```json
{
  "name": "City of Mississauga",
  "type": "root",
  "fiscal_year": 2025,
  "children": [
    {
      "name": "General Government",
      "type": "department",
      "children": [
        {
          "name": "Operating",
          "type": "dataset",
          "children": [
            {
              "name": "<category name>",
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
  ]
}

Extraction guidelines

Use the table only — ignore any notes, subtitles, totals, or headers.

Normalize names (trim, capitalize properly, remove extra spaces).

Convert all numbers to integers (strip commas and $).

The output file should be valid JSON, indented, UTF-8 encoded.

Each category row (e.g., “Labour”) becomes one object in "children".

Example Output
{
  "name": "City of Mississauga",
  "type": "root",
  "fiscal_year": 2025,
  "children": [
    {
      "name": "General Government",
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
                { "name": "2023", "type": "year", "amount": 57313 },
                { "name": "2024", "type": "year", "amount": 64171 },
                { "name": "2025", "type": "year", "amount": 67121 }
              ]
            },
            {
              "name": "Staff Development",
              "type": "category",
              "children": [
                { "name": "2023", "amount": 650 },
                { "name": "2024", "amount": 741 },
                { "name": "2025", "amount": 818 }
              ]
            }
          ]
        }
      ]
    }
  ]
}

Cursor task template

Inside Cursor, run an agent instruction like:

Parse data/splits/page_204.pdf.
Detect the “Operating Budget Overview ($000s)” table.
Extract all rows into structured JSON using the schema above.
Save it as data/budget_2025_tree.json.

Validation step

After generation, check:

jq '.' data/budget_2025_tree.json


If it parses cleanly and starts with "City of Mississauga", you’re ready for the next loop phase (department extraction).

Next Phase (after validation)

Once budget_2025_tree.json exists,
future iterations will append new department sections (IT, Library, Fire, etc.) into the "children" array.

Each department follows the same structure as “General Government”.

End of Phase 1 instructions