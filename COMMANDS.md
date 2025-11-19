
# Docker comands

## Start containers
1. Run Docker containers

- docker compose up -d

2. List containers running. Ensure db container is running
  
  - docker ps

## Stop and rebuild containers

 - docker compose down
 - docker compose up --build


----------------------------------------------------------------------

# Install ython dependancies (if needed)

 - pip install dependencyName

 Install and Freeze Dependencies from requirements.txt (when needed)

   - pip freeze > requirements.txt

   - pip install -r requirements.txt



### Kill PORTS IN USE

list ports in used
 - lsof -i :7860

kill port
 - kill -9 <port>
