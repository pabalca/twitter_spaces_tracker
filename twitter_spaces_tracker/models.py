import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())



class Account(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    username = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Account> <{self.username}"


class Space(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    account_id = db.Column(db.String, db.ForeignKey(Account.id))
    account = db.relationship(Account, backref='spaces')
    title = db.Column(db.String)
    url = db.Column(db.String)
    participant_count = db.Column(db.Integer)
    state = db.Column(db.String)
    scheduled_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    state = db.Column(db.String)

    def __repr__(self):
        return f"<Space> <{self.title}> <{self.url}>"

