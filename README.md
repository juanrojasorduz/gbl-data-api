# gbl-data-api
The purpose of this REST API service is to receive new data for hired employees, jobs, and departments.


## Prerequisites:
- Python
- Docker
- Postman 
- DBeaver (Optional)

## Build and Run Containers
1. List all containers:
```
    docker ps -a
```
2. Run the Postgres container:
```
    docker compose up -d flask_db
```
3. List all containers to verify:
```
    docker ps -a
```
4. Build the docker Image:
```
    docker compose build
```
5. Run the docker container:
```
    docker compose up --build flask_app
```
## Prove all methods:
1. Hired Employees:
```
    [GET] localhost:4000/hired_employees    Gets all hired employees
    [GET] localhost:4000/hired_employees/{Id}   Gets a hired employee by Id 
    [POST] localhost:4000/hired_employees   Adds a batch of hired employees (1-1000)
    [PUT] localhost:4000/hired_employees/{Id}   Updates a hired employee by Id 
    [DELETE] localhost:4000/hired_employees/{Id}    Deletes a hired employee by Id    
```
2. Departments:
```
    [GET] localhost:4000/departments    Gets all departments
    [GET] localhost:4000/departments/{Id}   Gets a department by Id 
    [POST] localhost:4000/departments   Adds a batch of departments (1-1000)
    [PUT] localhost:4000/departments/{Id}   Updates a department by Id 
    [DELETE] localhost:4000/departments/{Id}    Deletes a department by Id    
```
3. Jobs:
```
    [GET] localhost:4000/jobs    Gets all jobs
    [GET] localhost:4000/jobs/{Id}   Gets a job by Id 
    [POST] localhost:4000/jobs   Adds a batch of jobs (1-1000)
    [PUT] localhost:4000/jobs/{Id}   Updates a job by Id 
    [DELETE] localhost:4000/jobs/{Id}    Deletes a job by Id    
```

Use folder data for body to load historical data, then you can do any changes needed.