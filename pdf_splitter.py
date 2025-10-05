from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("data/2025_Budget.pdf")
for i, page in enumerate(reader.pages, start=1):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"data/splits/page_{i:03}.pdf", "wb") as f:
        writer.write(f)
print("✅ All pages split individually.")
