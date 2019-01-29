from .. import db
from sqlalchemy_utils.types import TSVectorType


class Url(db.Model):
    __tablename__ = 'urls'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key = True)
    long_url = db.Column(db.Text, unique = True)
    short_url = db.Column(db.String(1000))
    domain = db.Column(db.String(1000))
    added_datetime = db.Column(db.DateTime)
    hash_long_url = db.Column(db.String(64))
    click_count = db.Column(db.Integer)

    # search_vector = db.Column(TSVectorType('long_url', 'short_url'))
    @property
    def serialize(self):
        dic =  {
            'id' : self.id,
            'long_url' : self.long_url,
            'short_url' : self.short_url,
            'domain' : self.domain,
            'added_datetime' : self.added_datetime.isoformat(),
            'hash_long_url' : self.hash_long_url,
            'click_count' : self.click_count
        }
        return dic