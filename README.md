# gbl-data-api
The purpose of this REST API service is to receive new data for hired employees, jobs, and departments.


## Prerequisites:
- Python
- Docker
- Postman 
- DBeaver (Optional)

## Build and Run Containers
1. List all containers:
    docker ps -a

2. Run the Postgres container:
    docker compose up -d flask_db

3. List all containers to verify:
    docker ps -a

4. Build the docker Image:
    docker compose build

5. Run the docker container:
    docker compose up --build flask_app

## Prove all methods:

get
localhost:4000/users
localhost:4000/users/1

post
localhost:4000/users
{
    "username":"Maria Perez",
    "email":"maria.perez@gmail.com"
}

update
localhost:4000/users/1
{
    "username":"Maria Perez",
    "email":"maria.perez@gmail.com"
}

delete
localhost:4000/users/2