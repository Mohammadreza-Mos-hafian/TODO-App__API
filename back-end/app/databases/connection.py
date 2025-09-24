from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from flask_marshmallow import Marshmallow

from dotenv import load_dotenv

import os

load_dotenv()

SECRET_KEY = os.getenv("secret_key").strip()
DEBUG = os.getenv("DEBUG") == "True"

DB_DOMAIN = f"{os.getenv('DB_DOMAIN').strip()}+{os.getenv('DB_DRIVER').strip()}"
DB_USER = f"{os.getenv("DB_USERNAME").strip()}:{os.getenv("DB_PASSWORD").strip()}"
DB_HOST = f"{os.getenv('DB_HOST').strip()}:{os.getenv('DB_PORT').strip()}"
DB_NAME = os.getenv("DB_NAME").strip()

DB_URL = f"{DB_DOMAIN}://{DB_USER}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

ma = Marshmallow()


class Base(DeclarativeBase):
    pass
