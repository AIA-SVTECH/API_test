from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://root:root@10.1.70.232:3306/svtech"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# conn = engine.connect()
# result = conn.execute(text("SELECT * FROM customers;"))
# for row in result:
#     print(row)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
