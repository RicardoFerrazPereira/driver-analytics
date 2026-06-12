import re

from datetime import date

import pandas as pd

from parser import extract_records

MONTHS = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12,
}


def classify_event(event_line: str):

    if "Valor extra" in event_line:
        return "TIP"

    if "Prioridade" in event_line:
        return "PRIORITY"

    return "RIDE"


def parse_money_values(event_line: str):

    matches = re.findall(r"(-?)R\$ ?([\d,]+)", event_line)

    values = []

    for sign, value in matches:

        amount = float(value.replace(",", "."))

        if sign == "-":
            amount *= -1

        values.append(amount)

    return values


def parse_time(time_str: str):

    if len(time_str) != 4:
        return None

    return f"{time_str[:2]}:{time_str[2:]}"


def parse_trip_date(event_line: str, report_year: int):

    match = re.search(r"(\d{1,2}) de ([a-z]{3})", event_line.lower())

    if not match:
        return None

    day = int(match.group(1))

    month_text = match.group(2).replace(".", "")

    month = MONTHS.get(month_text)

    if not month:
        return None

    return date(report_year, month, day)


def parse_detail_line(detail_line: str):

    numbers = re.findall(r"\d{4}", detail_line)

    balance_match = re.search(r"R\$ ([\d,]+)", detail_line)

    running_balance = None

    if balance_match:

        running_balance = float(balance_match.group(1).replace(",", "."))

    processed_time = None
    trip_time = None

    if len(numbers) >= 2:

        processed_time = parse_time(numbers[0])

        trip_time = parse_time(numbers[1])

    return {
        "processed_time": processed_time,
        "trip_time": trip_time,
        "running_balance": running_balance,
    }


def build_record(event_line, detail_line, report_year):

    event_type = classify_event(event_line)

    values = parse_money_values(event_line)

    detail_data = parse_detail_line(detail_line)

    gross_amount = None
    cash_received = None
    wallet_change = None

    if len(values) == 2:

        gross_amount = values[0]

        wallet_change = values[1]

    elif len(values) == 3:

        gross_amount = values[0]

        cash_received = abs(values[1])

        wallet_change = values[2]

    return {
        "platform": "uber",
        "trip_date": parse_trip_date(event_line, report_year),
        "event_type": event_type,
        "gross_amount": gross_amount,
        "cash_received": cash_received,
        "wallet_change": wallet_change,
        "processed_time": detail_data["processed_time"],
        "trip_time": detail_data["trip_time"],
        "running_balance": detail_data["running_balance"],
    }


def transform_pdf(pdf_path: str):

    raw_records, report_year = extract_records(pdf_path)

    records = []

    for row in raw_records:

        record = build_record(row["event_line"], row["detail_line"], report_year)

        records.append(record)

    return records


if __name__ == "__main__":

    records = transform_pdf("data/raw/uber/relatorio.pdf")

    print(f"\nTotal registros: {len(records)}\n")

    print("\nPrimeiros 5 registros:\n")

    for record in records[:5]:
        print(record)

    df = pd.DataFrame(records)

    print("\nDataFrame:")
    print(df.head())

    print("\nResumo:")
    print(df.describe())
