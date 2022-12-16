from database import db


# Assuming some arbitrary permission types:
PERMISSION_TYPES = [
    'NONE',
    'BASIC',
    'FULL'
]


class UserPermission(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, autoincrement=False)
    type = db.Column(db.String(20), primary_key=True)
    granted_date = db.Column(db.DateTime, nullable=False)


    def validate(self):
        return (self.user_id and 
                self.granted_date and 
                self.type and 
                self.type in PERMISSION_TYPES)


    def to_json(self):
        return {
            'user_id': self.user_id,
            'type': self.type,
            'granted_date': str(self.granted_date)
        }