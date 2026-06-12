import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(ROOT))

from sqlalchemy import text
from app.database.connection import engine


def total_revenue():

    query = """
    SELECT
        ROUND(SUM(gross_amount), 2)
    FROM trips
    WHERE event_type IN ('RIDE', 'PRIORITY')
    """

    with engine.connect() as conn:
        return conn.execute(text(query)).scalar()


def total_trips():

    query = """
    SELECT
        COUNT(*)
    FROM trips
    WHERE event_type IN ('RIDE', 'PRIORITY')
    """

    with engine.connect() as conn:
        return conn.execute(text(query)).scalar()


def average_ticket():

    query = """
    SELECT
        ROUND(AVG(gross_amount), 2)
    FROM trips
    WHERE event_type IN ('RIDE', 'PRIORITY')
    """

    with engine.connect() as conn:
        return conn.execute(text(query)).scalar()


def total_tips():

    query = """
    SELECT
        ROUND(SUM(gross_amount), 2)
    FROM trips
    WHERE event_type = 'TIP'
    """

    with engine.connect() as conn:
        return conn.execute(text(query)).scalar()


def cash_trips():

    query = """
    SELECT
        COUNT(*)
    FROM trips
    WHERE cash_received IS NOT NULL
    """

    with engine.connect() as conn:
        return conn.execute(text(query)).scalar()


def cash_received_total():

    query = """
    SELECT
        ROUND(SUM(cash_received), 2)
    FROM trips
    WHERE cash_received IS NOT NULL
    """

    with engine.connect() as conn:
        return conn.execute(text(query)).scalar()


def revenue_by_day():

    query = """
    SELECT
        trip_date,
        ROUND(SUM(gross_amount), 2) AS revenue
    FROM trips
    WHERE event_type IN ('RIDE', 'PRIORITY')
    GROUP BY trip_date
    ORDER BY trip_date
    """

    with engine.connect() as conn:

        result = conn.execute(text(query))

        return result.fetchall()


if __name__ == "__main__":

    print("=" * 50)
    print("DRIVER ANALYTICS")
    print("=" * 50)

    print(f"Receita Total: R$ {total_revenue()}")

    print(f"Total Corridas: {total_trips()}")

    print(f"Ticket Médio: R$ {average_ticket()}")

    print(f"Gorjetas: R$ {total_tips()}")

    print(f"Corridas Dinheiro: {cash_trips()}")

    print(f"Dinheiro Recebido: R$ {cash_received_total()}")

    print("\nReceita por dia:")

    for day, revenue in revenue_by_day():

        print(f"{day} -> R$ {revenue}")
