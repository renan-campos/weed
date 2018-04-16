"""
    Creates a database and defines a table in an object oriented manner.
"""
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from sqlalchemy import Date

DB_ENGINE = create_engine('sqlite:///dynamic/data.db', echo=True)
DB_BASE   = declarative_base()

class User(DB_BASE):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Enviro(DB_BASE):
    __tablename__ = "environment"

    id    = Column(Integer, primary_key=True)
    sdate = Column(String, default=datetime.today().strftime("%c"), nullable=False)
    # This will be used for graphing and compression later
    date = Column(Date, default=datetime.today(), nullable=False)
    temp  = Column(Float)
    hum   = Column(Float)
    moi   = Column(Float)

    def __init__(self, temp, hum, moi):
        self.temp = temp
        self.hum  = hum
        self.moi  = moi
        self.sdate = datetime.today().strftime("%c")
        self.date = datetime.today()

# Create tables (Only if table doesn't already exist!)
DB_BASE.metadata.create_all(DB_ENGINE)

# This will be used to make add, queries, deletes
Session = sessionmaker(bind=DB_ENGINE)

if __name__ == '__main__':
    s = Session()
    s.add(User("admin", "password"))
    s.commit()
