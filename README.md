
# Commands

### Create and run Python Environment

1. Ensure you're in a virtual environment. If you haven't created one, create it:
   bash

    - python3.10 -m venv venv   (VERSION 10 NEEDED, not 13)

2. Activate the virtual environment:

    - source venv/bin/activ# 🚀 To Run It


3. Install and Freeze Dependencies from requirements.txt:
   Install all the dependencies listed in your requirements.txt file:

   - pip freeze > requirements.txt

   - pip install -r requirements.txt


### Run Docker Containers

- docker compose up -d

- docker ps  (checks if contaner is running)

### Terminal 1: Run Backend
cd backend
uvicorn main:app --reload


### Kill ports in used

list ports in used
 - lsof -i :7860

kill port
 - kill -9 <port>


### Run Chroma for New Embeddings Source

Run Chroma(from root directory) to load datasource after changes in data

- python -m backend.data.index.chroma_index