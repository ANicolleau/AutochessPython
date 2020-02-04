from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:root@localhost:3306', echo=True)
engine.execute("CREATE DATABASE IF NOT EXISTS autochess")
engine.execute("USE autochess")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base = declarative_base()
