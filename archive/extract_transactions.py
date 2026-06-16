import re
import pdfplumber
import pandas as pd

pdf_path = "data/raw/uber/relatorio.pdf"

all_text = ""

transactions_started = False

print(all_text[:1000])

with pdfplumber.open(pdf_path) as pdf:

    for page in pdf.pages:

        text = page.extract_text()

        if text:

            if "Transações" in text:
                transactions_started = True

            if transactions_started:
                all_text += text + "\n"


pattern = r"(Uber X|Prioridade).*?R\$ ([\d,]+)"

matches = re.findall(pattern, all_text, re.DOTALL)

records = []

for trip_type, amount in matches:

    amount = float(amount.replace(",", "."))

    records.append({"trip_type": trip_type, "amount": amount})

df = pd.DataFrame(records)

print(df.head())

print("\n")

print(df.describe())
