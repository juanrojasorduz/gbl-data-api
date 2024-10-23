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
def get_object(id):
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
    if employee:
      data = request.get_json()
      employee.name = data['name']
      employee.datetime = data['datetime']
      employee.department_id = data['department_id']
      employee.job_id = data['job_id']
      db.session.commit()
      return make_response(jsonify({'message': 'employee updated'}), 200)
    return make_response(jsonify({'message': 'employee not found'}), 404)
  except e:
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