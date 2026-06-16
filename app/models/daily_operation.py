from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import String

from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class DailyOperation(Base):

    __tablename__ = "daily_operations"

    id = Column(Integer, primary_key=True)

    operation_date = Column(Date, nullable=False, unique=True)

    km_driven = Column(Numeric(10, 2))

    hours_worked = Column(Numeric(10, 2))

    fuel_cost = Column(Numeric(10, 2))

    notes = Column(String(255))

    created_at = Column(DateTime, server_default=func.now())
