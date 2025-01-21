from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from databases import Database

DATABASE_URL = "sqlite:///./shortener.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

urls = Table(
    "urls",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("original_url", String, nullable=False),
    Column("shortened_url", String, nullable=False, unique=True),
    Column("custom_alias", String, unique=True, nullable=True),
    Column("expiry_date", DateTime, nullable=True),
)

metadata.create_all(bind=engine)

database = Database(DATABASE_URL)
