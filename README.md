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