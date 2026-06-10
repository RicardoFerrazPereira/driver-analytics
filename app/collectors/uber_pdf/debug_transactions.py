import pdfplumber

pdf_path = "data/raw/uber/relatorio.pdf"

transactions_started = False

with pdfplumber.open(pdf_path) as pdf:

    for page_number, page in enumerate(pdf.pages):

        text = page.extract_text()

        if not text:
            continue

        if "Transações" in text:
            transactions_started = True

        if not transactions_started:
            continue

        print("\n")
        print("=" * 80)
        print(f"PÁGINA {page_number + 1}")
        print("=" * 80)

        lines = text.split("\n")

        for i, line in enumerate(lines):

            if "Uber X" in line:
                print(line)

            elif "Prioridade" in line:
                print(line)

            elif "Valor extra" in line:
                print(line)
