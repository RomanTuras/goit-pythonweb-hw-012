"""
Connect Module
"""

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "postgresql://postgres:fE512@localhost:5432/contacts"

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine)

session = Session()
