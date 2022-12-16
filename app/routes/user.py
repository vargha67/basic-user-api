from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from routes.user_permission import user_permission_routes


user_routes = Blueprint('user_routes', __name__)
user_routes.register_blueprint(user_permission_routes, url_prefix='/<int:user_id>/permissions')


''' List users and optionally filter by last name '''
@user_routes.route('/', methods=['GET'])
def list_users():
    last_name = request.args.get('last_name') if request.args else None
    query = db.select(User)
    if last_name:
        query = query.filter_by(last_name=last_name)

    query = query.order_by(User.last_name)
    users = None
    try:
        users = db.session.execute(query).scalars()
    except Exception as err:
        print(f'Database error in loading users: {err}')
        return 'Error in loading the users data!', 500

    users = users or []
    return jsonify([u.to_json() for u in users])


''' Get a user by id '''
@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if not user_id:
        return 'User ID not provided!', 400

    query = db.select(User).filter_by(id=user_id)
    user = None
    try: 
        user = db.session.execute(query).first()
        if not user: 
            return 'No user found with this ID!', 400
        user = user[0]
    except Exception as err:
        print(f'Database error in loading user with ID {user_id}: {err}')
        return 'Error in loading the user data!', 500

    return jsonify(user.to_json())
    

''' Add a new user '''
@user_routes.route('/', methods=['POST'])
def add_user():
    body = request.json if request.json else {}
    new_user = User(
        email=body.get('email'),
        first_name=body.get('first_name'),
        last_name=body.get('last_name'),
        birth_date=body.get('birth_date')
    )

    if not new_user.validate():
        return 'Invalid or incomplete user information!', 400

    query = db.select(User).filter_by(email=new_user.email)
    try: 
        user = db.session.execute(query).first()
        if user: 
            return 'A user with this email already exists!', 400

        db.session.add(new_user)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        print(f'Database error in saving the new user: {err}')
        return 'Error in saving the new user!', 500

    return jsonify(new_user.to_json())
    

''' Remove an existing user '''
@user_routes.route('/<int:user_id>', methods=['DELETE']) 
def remove_user(user_id):
    if not user_id:
        return 'User ID not provided!', 400

    query = db.select(User).filter_by(id=user_id)
    user = None
    try: 
        user = db.session.execute(query).first()
        if not user: 
            return 'No user found with this ID!', 400

        user = user[0]
        db.session.delete(user)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        print(f'Database error in removing the user: {err}')
        return 'Error in removing the user!', 500

    return jsonify(user.to_json())
