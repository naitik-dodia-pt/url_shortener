from .. import db

class freeURL(db.Model):
    __tablename__ = 'url_pool'
    short_url = db.Column(db.String(10), primary_key = True)