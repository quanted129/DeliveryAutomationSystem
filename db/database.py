from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Hide in separate file

SERVER_NAME = r"localhost"
DATABASE_NAME = "deliveries"
DRIVER_NAME = "ODBC Driver 17 for SQL Server"

SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://{SERVER_NAME}/{DATABASE_NAME}"
    f"?driver={DRIVER_NAME}&Trusted_Connection=yes"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass