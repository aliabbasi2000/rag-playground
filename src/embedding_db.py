"""
This module stores each sentence of our files as a different row in the database. 
It stores it along with its vector embedding, its position in the file, and the name of the file it comes from.
"""
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector

import os
from dotenv import load_dotenv

load_dotenv()
Base = declarative_base()

# setup a connection to the Postgres database
def get_psql_session():
    host = os.getenv("DB_HOST")
    db = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")

    engine = create_engine(f'postgresql://{user}:{password}@{host}/{db}')
    Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    return Session()

print(get_psql_session())