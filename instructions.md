# Budget Data PDF Splitter

This project contains a Python script to split a PDF file into individual pages.

## Setup Instructions

### 1. Activate Virtual Environment

**For macOS/Linux:**
```bash
source venv/bin/activate
```

**For Windows:**
```bash
venv\Scripts\activate
```

### 2. Install Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install PyPDF2
```

### 3. Run the PDF Splitter

```bash
python pdf_splitter.py
```

## What the Script Does

- Reads the PDF file from `data/2025_Budget.pdf`
- Splits each page into a separate PDF file
- Saves individual pages to `data/splits/` directory
- Names files as `page_001.pdf`, `page_002.pdf`, etc.

## File Structure

```
budget-data/
├── data/
│   ├── 2025_Budget.pdf      # Source PDF file
│   └── splits/              # Output directory for split pages
├── venv/                    # Virtual environment
├── pdf_splitter.py          # Main script
└── instructions.md          # This file
```

## Notes

- Make sure the virtual environment is activated before running the script
- The script will create the `data/splits/` directory if it doesn't exist
- Each page will be saved as a separate PDF file with zero-padded numbering

## Deactivating Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```
