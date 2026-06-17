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

#print(get_psql_session())

class TextEmbedding(Base):
    __tablename__ = "text_embeddings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    content = Column(String)
    file_name = Column(String)
    sentence_number = Column(Integer)

    def __str__(self):
        return self.content + " " + str(self.id)
    
def insert_embeddings(embeddings, contents, file_names, session):
    for embedding, content, file_name in zip(embeddings, contents, file_names):
        new_embedding = TextEmbedding(embedding=embedding, content=content, file_name=file_name)
        session.add(new_embedding)
    
    session.commit()

# TEST
if __name__ == "__main__":
    insert_embeddings([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]], ["Sample sentence.", "Sample sentence2."], ["test_file1.txt", "test_file2.txt"], get_psql_session())
    print("Sample embeddings inserted into the database.")