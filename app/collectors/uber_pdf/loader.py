import pandas as pd
import sys

from pathlib import Path
from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[3]

sys.path.append(str(ROOT))

from transformer import transform_pdf
from hash_utils import calculate_file_hash
from import_checker import import_already_exists

from app.database.connection import engine

PDF_PATH = "data/raw/uber/relatorio.pdf"


def save_import_history(
    file_name, file_hash, total_records, period_start, period_end, status="SUCCESS"
):
    query = text("""
        INSERT INTO import_history (
            file_name,
            file_hash,
            total_records,
            period_start,
            period_end,
            status
        )
        VALUES (
            :file_name,
            :file_hash,
            :total_records,
            :period_start,
            :period_end,
            :status
        )
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "file_name": file_name,
                "file_hash": file_hash,
                "total_records": total_records,
                "period_start": period_start,
                "period_end": period_end,
                "status": status,
            },
        )


def load_pdf():

    file_hash = calculate_file_hash(PDF_PATH)

    if import_already_exists(file_hash):

        print("\nArquivo já foi importado anteriormente.")
        print("Importação cancelada.\n")

        return

    records = transform_pdf(PDF_PATH)

    df = pd.DataFrame(records)

    df.to_sql("trips", con=engine, if_exists="append", index=False)

    period_start = df["trip_date"].min()
    period_end = df["trip_date"].max()

    save_import_history(
        file_name=Path(PDF_PATH).name,
        file_hash=file_hash,
        total_records=len(df),
        period_start=period_start,
        period_end=period_end,
    )

    print(f"\n{len(df)} registros inseridos com sucesso.")
    print("Importação registrada no histórico.\n")


if __name__ == "__main__":

    load_pdf()
