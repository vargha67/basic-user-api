import re
from datetime import datetime
from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    permissions = db.relationship('UserPermission', cascade="all, delete, delete-orphan")


    def validate(self): 
        if ((not self.email) or 
            (not self.first_name) or 
            (not self.last_name) or 
            (not self.birth_date)):
            return False

        try:
            self.birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d %H:%M:%S')
        except ValueError as ex:
            print(f'Incorrect date format: {ex}')
            return False

        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(email_regex, self.email):
            return False

        if self.permissions and (not all([p.validate() for p in self.permissions])):
            return False

        return True


    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name, 
            'last_name': self.last_name, 
            'birth_date': str(self.birth_date),
            'permissions': [p.to_json() for p in self.permissions] if self.permissions else []
        }

