
# DOCKER

### Run Docker containers

- docker compose up -d

- docker ps  (checks if contaner is running)


# BUILD DATABASE

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




# INSTAL DEPENDENCIES (if needed)

 - pip install dependencyName

 Install and Freeze Dependencies from requirements.txt (when needed)

   - pip freeze > requirements.txt

   - pip install -r requirements.txt



### Terminal 1: RUN BACKEND

cd backend
uvicorn main:app --reload



### Kill PORTS IN USE

list ports in used
 - lsof -i :7860

kill port
 - kill -9 <port>
