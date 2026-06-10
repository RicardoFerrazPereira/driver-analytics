from app.models.trip import Base
from app.database.connection import engine

Base.metadata.create_all(engine)

print("Tabelas criadas.")
