import pdfplumber

pdf_path = "data/raw/uber/relatorio.pdf"

with pdfplumber.open(pdf_path) as pdf:

    print(f"Total de páginas: {len(pdf.pages)}")

    for page_number, page in enumerate(pdf.pages):

        text = page.extract_text()

        print("=" * 50)
        print(f"Página {page_number + 1}")
        print("=" * 50)

        print(text)
