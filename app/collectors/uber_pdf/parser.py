import re
import pdfplumber


def clean_text(text: str) -> str:
    return text.replace("\x00", "")


def extract_records(pdf_path: str):

    transactions_started = False

    lines = []

    report_year = None

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if not text:
                continue

            # Extrai o ano apenas uma vez
            if report_year is None:

                year_match = re.search(r"de (\d{4})", text)

                if year_match:
                    report_year = int(year_match.group(1))

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

        detail_line = ""

        if i + 1 < len(lines):
            detail_line = lines[i + 1]

        records.append({"event_line": line, "detail_line": detail_line})

        i += 2

    return records, report_year


if __name__ == "__main__":

    records, report_year = extract_records("data/raw/uber/relatorio.pdf")

    print(f"Ano do relatório: {report_year}")

    print(f"Total registros: {len(records)}")

    print(records[:3])
