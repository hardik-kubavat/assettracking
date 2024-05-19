from project.extention import db
from datetime import datetime

#Users
class Locater(db.Model):
    __tablename__ = 'locater'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    description = db.Column(db.String(),nullable=True)
    products = db.relationship('Product',backref='locater',lazy='dynamic')
    transactions = db.relationship('Transaction',backref='locater',lazy='dynamic')
    isdeleted = db.Column(db.Boolean(create_constraint=True, name="isdeletedcheck"))
    created_at = db.Column(db.TIMESTAMP(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @property
    def serialize(self):
        return {
            'id' : str(self.id),
            'name':self.name,
            'description':self.description,
            'isdeleted':self.isdeleted,
        }
    
    def __init__(self, name,description,isdeleted=False):
        self.name = name
        self.description = description
        self.isdeleted = isdeleted

    def __repr__(self):
        return '<Locater {}>'.format(self.name)
    
    def setName(self, name):
        self.name = name
    
    def setDescription(self, description):
        self.description = description
    
def getAll():
    return Locater.query.all()

def getById(locater_id):
    return Locater.query.filter_by(id=locater_id).first()