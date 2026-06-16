import pdfplumber

pdf_path = "data/raw/uber/relatorio.pdf"

transactions_started = False

transaction_lines = []

with pdfplumber.open(pdf_path) as pdf:

    for page in pdf.pages:

        text = page.extract_text()

        if not text:
            continue

        if "Transações" in text:
            transactions_started = True

        if not transactions_started:
            continue

        lines = text.split("\n")

        for line in lines:

            if "Uber X" in line or "Prioridade" in line or "Valor extra" in line:
                transaction_lines.append(line)

print(f"Total eventos: {len(transaction_lines)}")

for line in transaction_lines[:5]:
    print(line)
