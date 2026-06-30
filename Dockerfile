FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

COPY . .

CMD ["sh", "-c", "python src/generate_corpus.py && python src/populate_vector_db.py && exec python main.py"]
