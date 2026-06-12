# 1. Terminal A: start Ollama

```
curl -fsSL https://ollama.com/install.sh | sh 
ollama pull qwen3:0.6b
ollama pull nomic-embed-text
ollama serve
```
## Run model and Test it

```ollama run qwen3:0.6b```

# 2. Terminal B: activate venv 

python3 -m venv .venv
```source .venv/bin/activate```
nano .env
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=qwen3:0.6b

# 3. Developement Loop

## 1. Edit code and Run code locally with venv:
```python3 main.py```

## 2. When it works locally, Run inside Docker container 
```docker compose up --build```


