# gbl-data-api
Big data migration to a new database system

## Prerequisites:
*Python
*PostgreSQL 
*Docker
*Postman (Optional)
*DBeaver (Optional)

## Build and Run Containers
List all containers:
docker ps -a

Run the Postgres container:
docker compose up -d flask_db

List all containers to verify:
docker ps -a

Build the docker Image:
docker compose build

Run the docker container:
docker compose up flask_app
docker compose up --build flask_app

Once app is running:

Test endpoint:
http://localhost:4000/test

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