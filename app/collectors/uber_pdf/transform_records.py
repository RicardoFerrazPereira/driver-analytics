import re
from pprint import pprint


def classify_event(event_line: str) -> str:

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


def build_record(event_line, detail_line):

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
        "event_type": event_type,
        "gross_amount": gross_amount,
        "cash_received": cash_received,
        "wallet_change": wallet_change,
        "processed_time": detail_data["processed_time"],
        "trip_time": detail_data["trip_time"],
        "running_balance": detail_data["running_balance"],
    }


if __name__ == "__main__":

    event_line = "sáb., 30 de mai. " "Uber X R$ 14,63 " "-R$ 13,95 " "R$ 0,68"

    detail_line = "1905 30 de mai. " "1853 R$ 226,51"

    record = build_record(event_line, detail_line)

    pprint(record)
