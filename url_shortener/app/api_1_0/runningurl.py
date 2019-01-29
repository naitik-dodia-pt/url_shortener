from .. import db

class RunningURL(db.Model):
    __tablename__ = 'running_id'
    current_id = db.Column(db.Integer, primary_key = True)