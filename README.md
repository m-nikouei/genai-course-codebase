# Installation
1. Create a pytohn env:
```python -m venv .venv/env_name```
2. Install requirements:
```pip install -r requirements.txt```
3. Add keys to config file:
```json
{
    "chatbot": {
        "GOOGLE_API_KEY": "",
        "OPENAI_API_KEY":""
    }
}
```
4. Activate env:
```source .venv/env-name/bin/activate```
```& .venv\env-name\Scripts\activate```
# Run flask-chatbot
execute 
```python flask-chatbot/app.py```

# RAG Tool
* **Qdrant Server:**
1. Create your local storage for qdrant, e.g "/home/username/qdrant_data"
2. Run the server ```podman run -p 6333:6333 -v /home/username/qdrant_data:/qdrant/storage docker.io/qdrant/qdrant```.
* **Indexing:**
1. Go to ```bot/rag_indexing```
2. run ```python indexing.py [url]```. For our example, url by ```https://lilianweng.github.io/posts/2023-06-23-agent/```
