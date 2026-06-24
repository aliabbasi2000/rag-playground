from embedding_db import get_psql_session, TextEmbedding
from ollama import Client
from nltk.tokenize import sent_tokenize
from sqlalchemy import text
import os

query = "What is the human rights situation in Slovakia?"

host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
client = Client(host=host)

sentences = sent_tokenize(query)
embeddings = client.embed(model="nomic-embed-text", input=sentences)["embeddings"]
#print(embeddings[0])

# Find the most similar sentence in the database to our query using cosine distance
def search_embeddings(query_embedding, session, limit=5):
    
    # <=> operator for computing cosine distance between the query and the embeddings stored in the database
    # <=> expects both operands to be of type vector. So the query_embedding which is a python vector needs to be cast to vector type using CAST()
    sql_query = text("""
        SELECT id, sentence_number, content, file_name, 
                    embedding <=> CAST(:query_embedding AS vector) AS distance
        FROM text_embeddings
        ORDER BY distance
        LIMIT :limit
    """)

    result = session.execute(sql_query, {"query_embedding": query_embedding, "limit": limit})
    return result.fetchall()

def get_surrounding_sentences(entry_ids, file_names, session, group_window_size=3):
    surrounding_sentences = []
    
    # Fetch the entire surrounding window in a single query per entry_id to reduce the number of queries to the database
    for entry_id, file_name in zip(entry_ids, file_names):
        sql_query = text("""
            SELECT id, sentence_number, content, file_name
            FROM text_embeddings
            WHERE id >= :min_id AND id <= :max_id AND file_name = :file_name
        """)
        
        result = session.execute(sql_query, {
            "min_id": entry_id - group_window_size, 
            "max_id": entry_id + group_window_size,
            "file_name": file_name
        })
        
        surrounding_sentences.append(result.fetchall())

    return surrounding_sentences

if __name__ == "__main__":
    session = get_psql_session()
    query_result = search_embeddings(query_embedding=embeddings[0], session=session, limit=5)

    print("########## Query Result ##########")
    for row in query_result:
        print(f"ID: {row.id}, Sentence Number: {row.sentence_number}, File Name: {row.file_name}, Distance: {row.distance}")

    print("\n########## Surrounding Sentences for each Query Result ##########")
    entry_ids = []
    file_names = []
    for row in query_result:
        entry_ids.append(row.id)
        file_names.append(row.file_name)
    
    surrounding_sentences = get_surrounding_sentences(entry_ids=entry_ids, file_names=file_names, session=session, group_window_size=3)
    for entry_id, surrounding in zip(entry_ids, surrounding_sentences):
        print(f"Surrondings for {entry_id}:")
        for row in surrounding:
            print(f"ID: {row.id}, Sentence Number: {row.sentence_number}, Content: {row.content}, File Name: {row.file_name} \n")