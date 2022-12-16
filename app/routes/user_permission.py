from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from models.user_permission import UserPermission


user_permission_routes = Blueprint('user_permission_routes', __name__)


''' Add (grant) permission to user '''
@user_permission_routes.route('/', methods=['POST'])
def add_user_permission(user_id):
    if not user_id:
        return 'User ID not provided!', 400

    body = request.json if request.json else {}
    new_perm = UserPermission( \
        user_id=user_id, \
        type=body.get('type'), \
        granted_date=datetime.utcnow() \
    )

    if not new_perm.validate():
        return 'Invalid or incomplete permission information!', 400

    query = db.select(User).filter_by(id=user_id)
    try: 
        user = db.session.execute(query).first()
        if not user: 
            return 'No user found with this ID!', 400

        user = user[0]
        perms = user.permissions or []
        if any([p.type == new_perm.type for p in perms]):
            return 'This permission already granted to the user!', 400

        user.permissions.append(new_perm)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        print(f'Database error in adding permission to user: {err}')
        return 'Error in granting permission to user!', 500

    return jsonify(new_perm.to_json())


''' Remove (revoke) permission from user '''
@user_permission_routes.route('/<string:type>', methods=['DELETE'])
def remove_user_permission(user_id, type):
    if (not user_id) or (not type):
        return 'User ID or permission type not provided!', 400

    query = db.select(User).filter_by(id=user_id)
    perm = None
    try: 
        user = db.session.execute(query).first()
        if not user: 
            return 'No user found with this ID!', 400

        user = user[0]
        perms = user.permissions or []
        for p in perms:
            if p.type == type:
                perm = p
                break

        if not perm: 
            return 'This permission has not been granted to this user!', 400

        user.permissions.remove(perm)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        print(f'Database error in removing permission from user: {err}')
        return 'Error in revoking permission from user!', 500

    return jsonify(perm.to_json())