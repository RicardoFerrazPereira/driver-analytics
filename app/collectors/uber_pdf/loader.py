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

PDF_FOLDER = "data/raw/uber"


def save_import_history(
    file_name,
    file_hash,
    total_records,
    period_start,
    period_end,
    status="SUCCESS",
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


def insert_trips(records):

    query = text("""
        INSERT INTO trips (
            platform,
            trip_date,
            event_type,
            gross_amount,
            cash_received,
            wallet_change,
            processed_time,
            trip_time,
            running_balance,
            trip_hash
        )
        VALUES (
            :platform,
            :trip_date,
            :event_type,
            :gross_amount,
            :cash_received,
            :wallet_change,
            :processed_time,
            :trip_time,
            :running_balance,
            :trip_hash
        )
        ON CONFLICT (trip_hash)
        DO NOTHING
    """)

    inserted = 0

    with engine.begin() as conn:

        for record in records:

            result = conn.execute(query, record)

            inserted += result.rowcount

    return inserted


def load_pdf(pdf_path):

    file_hash = calculate_file_hash(pdf_path)

    if import_already_exists(file_hash):

        print(f"\n⏭ Arquivo já importado: {Path(pdf_path).name}")

        return {
            "imported": False,
            "records": 0,
            "ignored": 0,
        }

    records = transform_pdf(pdf_path)

    if not records:

        print(f"\n⚠ Nenhum registro encontrado em {Path(pdf_path).name}")

        return {
            "imported": False,
            "records": 0,
            "ignored": 0,
        }

    df = pd.DataFrame(records)

    inserted_count = insert_trips(records)

    ignored_count = len(records) - inserted_count

    period_start = df["trip_date"].min()
    period_end = df["trip_date"].max()

    save_import_history(
        file_name=Path(pdf_path).name,
        file_hash=file_hash,
        total_records=inserted_count,
        period_start=period_start,
        period_end=period_end,
    )

    print(f"\n✓ {Path(pdf_path).name}")
    print(f"  Registros encontrados: {len(records)}")
    print(f"  Novos registros: {inserted_count}")
    print(f"  Registros ignorados: {ignored_count}")

    return {
        "imported": True,
        "records": inserted_count,
        "ignored": ignored_count,
    }


def load_all_pdfs():

    pdf_files = sorted(Path(PDF_FOLDER).glob("*.pdf"))

    if not pdf_files:

        print("\nNenhum PDF encontrado.\n")

        return

    total_pdfs = len(pdf_files)
    imported_pdfs = 0
    total_records = 0
    total_ignored = 0

    print("\n" + "=" * 50)
    print("DRIVER ANALYTICS IMPORTER")
    print("=" * 50)

    for index, pdf_file in enumerate(pdf_files, start=1):

        print(f"\n[{index}/{total_pdfs}] Processando: {pdf_file.name}")

        result = load_pdf(str(pdf_file))

        if result["imported"]:
            imported_pdfs += 1

        total_records += result["records"]
        total_ignored += result["ignored"]

    print("\n" + "=" * 50)
    print("RESUMO FINAL")
    print("=" * 50)

    print(f"PDFs encontrados: {total_pdfs}")
    print(f"PDFs importados: {imported_pdfs}")
    print(f"Novos registros: {total_records}")
    print(f"Registros ignorados: {total_ignored}")

    print("\nImportação finalizada.\n")


if __name__ == "__main__":

    load_all_pdfs()
