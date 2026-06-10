import psycopg2
import time
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



#Connecting Database directly using psycopg2 without sqlalchemy
# while True:
#     try:
#         conn = psycopg2.connect(host= 'localhost',database='Fastapi',user='postgres',
#         password='Ashumylove',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("database connection successful")
#         break
#     except Exception as error:
#         print("database connection fail")
#         print(error)
#         time.sleep(2)
