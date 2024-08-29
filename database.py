from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# conn = engine.connect()
# result = conn.execute(text("SELECT * FROM customers;"))
# for row in result:
#     print(row)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
