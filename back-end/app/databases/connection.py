from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from dotenv import load_dotenv

import os

load_dotenv()

DB_DOMAIN = f"{os.getenv('DB_DOMAIN').strip()}+{os.getenv('DB_DRIVER').strip()}"
DB_USER = f"{os.getenv("DB_USERNAME").strip()}:{os.getenv("DB_PASSWORD").strip()}"
DB_HOST = f"{os.getenv('DB_HOST').strip()}:{os.getenv('DB_PORT').strip()}"
DB_NAME = os.getenv("DB_NAME").strip()

DB_URL = f"{DB_DOMAIN}://{DB_USER}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
