import pandas as pd
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

sys.path.append(str(ROOT))

from transformer import transform_pdf

from app.database.connection import engine

PDF_PATH = "data/raw/uber/relatorio.pdf"


def load_pdf():

    records = transform_pdf(PDF_PATH)

    df = pd.DataFrame(records)

    df.to_sql("trips", con=engine, if_exists="append", index=False)

    print(f"{len(df)} registros inseridos com sucesso.")


if __name__ == "__main__":

    load_pdf()
