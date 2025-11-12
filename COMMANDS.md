
### CREATE AND RUN PYTHON EVIRONMENT

1. Ensure you're in a virtual environment. If you haven't created one, create it:
   bash

    - python3.10 -m venv venv   (VERSION 10 NEEDED, not 13)

2. Activate the virtual environment:

    - source venv/bin/activ# 🚀 To Run It


3. Install and Freeze Dependencies from requirements.txt:
   Install all the dependencies listed in your requirements.txt file:

   - pip freeze > requirements.txt

   - pip install -r requirements.txt


### RUN DOCKER CONTAINERS

- docker compose up -d

- docker ps  (checks if contaner is running)


### INSTAL DEPENDENCIES

 - pip install fastmcp uvicorn pydantic chromadb

 3. Install and Freeze Dependencies from requirements.txt (when needed)

   - pip freeze > requirements.txt

   - pip install -r requirements.txt



### Terminal 1: RUN BACKEND

cd backend
uvicorn main:app --reload



### RUN CHROMA FOR NEW Embeddingd Source

Run Chroma(from root directory) to load datasource after changes in data

- python -m backend.data.index.chroma_index


### BUILD DATABASE

1. Start docker if not running

  - docker-compose up -d

2. List containers running and take the db container name for next step
  
  - docker ps
 
3. Copy the seed file into the container. Replace the database conatinername 

  - docker cp backend/mcps/db_analytics/db/seed.sql databaseName:/tmp/seed.sql

4. Load products to db container

 - docker exec -it retailbrain---be-db-1 psql -U hackathon_user -d mydatabase -f /tmp/seed.sql

5. Verify tables 

- docker exec -it retailbrain---be-db-1 psql -U hackathon_user -d mydatabase -c "\dt"

### ACCESS DB FROM CLI

 - docker compose exec db psql -U hackathon_user -d mydatabase
 
 - SELECT NOW();


### Kill PORTS IN USE

list ports in used
 - lsof -i :7860

kill port
 - kill -9 <port>
