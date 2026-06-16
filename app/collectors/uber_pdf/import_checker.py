from sqlalchemy import text

from app.database.connection import engine


def import_already_exists(file_hash):
    """
    Verifica se o PDF já foi importado.
    """

    query = text("""
        SELECT COUNT(*)
        FROM import_history
        WHERE file_hash = :file_hash
    """)

    with engine.connect() as conn:

        result = conn.execute(query, {"file_hash": file_hash})

        count = result.scalar()

    return count > 0
