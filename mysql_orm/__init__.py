from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker,Session
from dotenv import load_dotenv
import mysql.connector
import os

from mysql_orm.models import Accounts

load_dotenv()

MYSQL_URI = str(os.getenv("MYSQL_URI"))

engine = create_engine(MYSQL_URI)

session = Session(engine)





