import pdfplumber
import re
from pprint import pprint


def clean_text(text: str) -> str:
    return text.replace("\x00", "")


pdf_path = "data/raw/uber/relatorio.pdf"

transactions_started = False

lines = []

with pdfplumber.open(pdf_path) as pdf:

    for page in pdf.pages:

        text = page.extract_text()

        if not text:
            continue

        if "Transações" in text:
            transactions_started = True

        if not transactions_started:
            continue

        page_lines = text.split("\n")

        for line in page_lines:

            line = clean_text(line.strip())

            if not line:
                continue

            if (
                "Relatório semanal" in line
                or "Processado Evento" in line
                or "Ricardo Ferraz Pereira" in line
            ):
                continue

            lines.append(line)

records = []

i = 0

while i < len(lines):

    line = lines[i]

    is_event = "Uber X" in line or "Prioridade" in line or "Valor extra" in line

    if not is_event:
        i += 1
        continue

    record = {"event_line": line}

    # próxima linha
    detail_line = ""

    if i + 1 < len(lines):
        detail_line = lines[i + 1]

    record["detail_line"] = detail_line

    records.append(record)

    i += 2

print(f"\nTotal registros encontrados: {len(records)}\n")

for record in records[:10]:
    pprint(record)
    print("-" * 80)
