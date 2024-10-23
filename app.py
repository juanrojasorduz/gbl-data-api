from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'username': self.username, 'email': self.email}

db.create_all()

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

# create a user
@app.route('/users', methods=['POST'])
def create_users(): 
    try: 
        data = request.get_json()        
        if not isinstance(data, list):
            return make_response(jsonify({'message': 'Invalid input, expected a list of users'}), 400)        
        if len(data) < 1 or len(data) > 1000:
            return make_response(jsonify({'message': 'Number of users must be between 1 and 1000'}), 400)

        new_users = []
        for user_data in data:
            if 'username' not in user_data or 'email' not in user_data:
                return make_response(jsonify({'message': 'Each user must have a username and email'}), 400)
            
            new_user = User(username=user_data['username'], email=user_data['email'])
            new_users.append(new_user)

        db.session.bulk_save_objects(new_users)
        db.session.commit()

        return make_response(jsonify({'message': 'users created', 'count': len(new_users)}), 201) 
    except Exception as e: 
        db.session.rollback()
        return make_response(jsonify({'message': 'error creating users', 'error': str(e)}), 500)

# get all users
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify([user.json() for user in users]), 200)
  except e:
    return make_response(jsonify({'message': 'error getting users'}), 500)

# get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting user'}), 500)

# update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.username = data['username']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error updating user'}), 500)

# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting user'}), 500)