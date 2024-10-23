from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class HiredEmployees(db.Model):
    __tablename__ = 'hired_employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    datetime = db.Column(db.String(120), unique=True, nullable=False)
    department_id = db.Column(db.String(120), unique=True, nullable=False)
    job_id = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'name': self.name, 'datetime': self.datetime, 'department_id': self.department_id, 'job_id': self.job_id}

class Departments(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'department': self.department}

class Jobs(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'job': self.job}                

db.create_all()


####### HIRED EMPLOYEES
# create a user
@app.route('/hired_employees', methods=['POST'])
def create_object(): 
    try: 
        data = request.get_json()        
        if not isinstance(data, list):
            return make_response(jsonify({'message': 'Invalid input, expected a list of Hired Employees'}), 400)        
        if len(data) < 1 or len(data) > 1000:
            return make_response(jsonify({'message': 'Number of Hired Employees must be between 1 and 1000'}), 400)

        new_objects = []
        for object_data in data:
            if 'name' not in object_data or 'datetime' not in object_data or 'department_id' not in object_data or 'job_id' not in object_data:
                return make_response(jsonify({'message': 'Each Hired Employee must have a username and email'}), 400)
            
            new_object = HiredEmployees(name=object_data['name'], datetime=object_data['datetime'], department_id=object_data['department_id'], job_id=object_data['job_id'])
            new_objects.append(new_object)

        db.session.bulk_save_objects(new_objects)
        db.session.commit()

        return make_response(jsonify({'message': 'Hired employee created', 'count': len(new_objects)}), 201) 
    except Exception as e: 
        db.session.rollback()
        return make_response(jsonify({'message': 'error creating Hired employee', 'error': str(e)}), 500)

# get all hired employees
@app.route('/hired_employees', methods=['GET'])
def get_object():
  try:
    hired_employees = HiredEmployees.query.all()
    return make_response(jsonify([employee.json() for employee in hired_employees]), 200)
  except e:
    return make_response(jsonify({'message': 'error getting hired employees'}), 500)

# get a hired employee by id
@app.route('/hired_employees/<int:id>', methods=['GET'])
def get_object_by_id(id):
  try:
    employee = HiredEmployees.query.filter_by(id=id).first()
    if employee:
      return make_response(jsonify({'employee': employee.json()}), 200)
    return make_response(jsonify({'message': 'employee not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting employee'}), 500)

# update a hired employee
@app.route('/hired_employees/<int:id>', methods=['PUT'])
def update_object(id):
    try:
        employee = HiredEmployees.query.filter_by(id=id).first()
        if not employee:
            return make_response(jsonify({'message': 'employee not found'}), 404)

        data = request.get_json()
        if not isinstance(data, dict):
            return make_response(jsonify({'message': 'Invalid input format, expected JSON object'}), 400)

        employee.name = data.get('name', employee.name)
        employee.datetime = data.get('datetime', employee.datetime)
        employee.department_id = data.get('department_id', employee.department_id)
        employee.job_id = data.get('job_id', employee.job_id)

        db.session.commit()
        return make_response(jsonify({'message': 'employee updated'}), 200)

    except Exception as e:
        print(f"Error updating employee: {e}")  
        return make_response(jsonify({'message': 'error updating employee'}), 500)

# delete a hired employee
@app.route('/hired_employees/<int:id>', methods=['DELETE'])
def delete_object(id):
  try:
    employee = HiredEmployees.query.filter_by(id=id).first()
    if employee:
      db.session.delete(employee)
      db.session.commit()
      return make_response(jsonify({'message': 'employee deleted'}), 200)
    return make_response(jsonify({'message': 'employee not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting employee'}), 500)



####### DEPARTMENTS
# create a department
@app.route('/departments', methods=['POST'])
def create_object_departments(): 
    try: 
        data = request.get_json()        
        if not isinstance(data, list):
            return make_response(jsonify({'message': 'Invalid input, expected a list of departments'}), 400)        
        if len(data) < 1 or len(data) > 1000:
            return make_response(jsonify({'message': 'Number of departments must be between 1 and 1000'}), 400)

        new_objects = []
        for object_data in data:
            if 'department' not in object_data:
                return make_response(jsonify({'message': 'Each department must have a department name'}), 400)
            
            new_object = Departments(name=object_data['department'])
            new_objects.append(new_object)

        db.session.bulk_save_objects(new_objects)
        db.session.commit()

        return make_response(jsonify({'message': 'department created', 'count': len(new_objects)}), 201) 
    except Exception as e: 
        db.session.rollback()
        return make_response(jsonify({'message': 'error creating department', 'error': str(e)}), 500)

# get all departments
@app.route('/departments', methods=['GET'])
def get_object_departments():
  try:
    departments = Departments.query.all()
    return make_response(jsonify([department.json() for department in departments]), 200)
  except e:
    return make_response(jsonify({'message': 'error getting department'}), 500)

# get a department by id
@app.route('/departments/<int:id>', methods=['GET'])
def get_object_by_id_departments(id):
  try:
    department = Departments.query.filter_by(id=id).first()
    if department:
      return make_response(jsonify({'department': department.json()}), 200)
    return make_response(jsonify({'message': 'department not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting department'}), 500)

# update a department by id
@app.route('/departments/<int:id>', methods=['PUT'])
def update_object_departments(id):
    try:
        department = Departments.query.filter_by(id=id).first()
        if not department:
            return make_response(jsonify({'message': 'department not found'}), 404)

        data = request.get_json()
        if not isinstance(data, dict):
            return make_response(jsonify({'message': 'Invalid input format, expected JSON object'}), 400)

        department.department = data.get('department', department.department)
        db.session.commit()
        return make_response(jsonify({'message': 'department updated'}), 200)

    except Exception as e:
        print(f"Error updating department: {e}")  
        return make_response(jsonify({'message': 'error updating department'}), 500)

# delete a department by id
@app.route('/departments/<int:id>', methods=['DELETE'])
def delete_object_departments(id):
  try:
    department = Departments.query.filter_by(id=id).first()
    if department:
      db.session.delete(department)
      db.session.commit()
      return make_response(jsonify({'message': 'department deleted'}), 200)
    return make_response(jsonify({'message': 'department not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting department'}), 500)
