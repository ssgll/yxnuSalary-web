from . import db
from flask_login import UserMixin


class User(UserMixin,db.Model):
    
    __bind_key__ = "local_db"
    __tablename__ = "salary_user"

    user_id = db.Column(db.String(16),primary_key=True,autoincrement=False)
    name = db.Column(db.String(16),nullable=False)
    password = db.Column(db.String(512))
    last_login = db.Column(db.Date())

    def get_id(self):
        return self.user_id
    
    def __repr__(self):
        return f"<User: name=>{self.name} email=>{self.user_id}>"
    
