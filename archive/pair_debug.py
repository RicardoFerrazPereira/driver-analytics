import pdfplumber

pdf_path = "data/raw/uber/relatorio.pdf"

transactions_started = False

event_lines = []

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
                event_lines.append(line)

            elif len(line) > 10 and line[:4].isdigit():
                event_lines.append(line)

for i in range(0, min(20, len(event_lines)), 2):

    print("\n" + "=" * 60)

    print("EVENTO:")
    print(event_lines[i])

    print("\nDETALHE:")
    print(event_lines[i + 1])
