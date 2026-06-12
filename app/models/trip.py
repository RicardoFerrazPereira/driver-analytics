from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime

from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Trip(Base):

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)

    platform = Column(String(20), nullable=False, index=True)

    trip_date = Column(Date, index=True)

    processed_time = Column(String(5))

    trip_time = Column(String(5))

    event_type = Column(String(100), index=True)

    gross_amount = Column(Numeric(10, 2))

    cash_received = Column(Numeric(10, 2))

    wallet_change = Column(Numeric(10, 2))

    running_balance = Column(Numeric(10, 2))

    created_at = Column(DateTime, server_default=func.now())
