from flaskr import db, loginmanager
from flask_login import UserMixin


@loginmanager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True, unique=True)
    fname = db.Column('fname', db.Unicode, nullable=False)
    mname = db.Column('mname', db.Unicode)
    lname = db.Column('lname', db.Unicode)
    dob = db.Column('dob', db.Date)
    email = db.Column('email', db.Unicode, unique=True, nullable=False)
    phone = db.Column('phone', db.Unicode)
    password = db.Column('password', db.Unicode, nullable=False)
    sex = db.Column('sex_id', db.Integer)
    active = db.Column('active', db.Integer)

    def __repr__(self):
        return f"Users('{self.fname}','{self.email}','{self.password}')"
