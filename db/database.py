import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

SERVER_NAME = os.getenv("DB_SERVER_NAME")
DATABASE_NAME = os.getenv("DB_DATABASE_NAME")
DRIVER_NAME = os.getenv("DB_DRIVER_NAME")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

if DB_PASSWORD:
    SQLALCHEMY_DATABASE_URL = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{SERVER_NAME}/{DATABASE_NAME}"
        f"?driver={DRIVER_NAME}&TrustServerCertificate=yes"
    )
else:
    SQLALCHEMY_DATABASE_URL = (
        f"mssql+pyodbc://{SERVER_NAME}/{DATABASE_NAME}"
        f"?driver={DRIVER_NAME}&Trusted_Connection=yes"
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()