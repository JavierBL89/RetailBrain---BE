
# DOCKER

### Run Docker containers

- docker compose up -d

- docker ps  (checks if contaner is running)


# INSTAL PYTHON DEPENDENCIES (if needed)

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
