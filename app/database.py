from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    create_db(app)

def create_db(app):
    with app.app_context():
        db.create_all()

def drop_db(app):
    db.drop_all()

def remove_all_data():
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
