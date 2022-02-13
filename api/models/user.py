from ..utils.db import db

class User(db.Model):
    username= db.Column(db.String, primary_key=True)
    first_name=db.Column(db.String)
    last_name=db.Column(db.String)
    user_type=db.Column(db.String)
    street= db.Column(db.String)
    city= db.Column(db.String)
    state=db.Column(db.String)
    zip_code= db.Column(db.String)
    parent= db.Column(db.String)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}