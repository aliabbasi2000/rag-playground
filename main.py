import os
from ollama import Client

host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
client = Client(host=host)

embeddings = client.embed(model="nomic-embed-text", input=["Here is an example sentence I will be embedding!", "Here's a second one!"])

print(len(embeddings['embeddings']))

response = client.chat(model='qwen3:0.6b', messages=[
  {
    'role': 'user',
    'content': 'Why did the chicken cross the road?',
  },
])

print(response.message.content)