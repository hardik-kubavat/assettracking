from project.extention import db
from datetime import datetime

class ProductType(db.Model):
    __tablename__ = 'product_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    description = db.Column(db.String(),nullable=True)
    categories = db.relationship('Category',backref='producttype',lazy='dynamic')
    products = db.relationship('Product',backref='producttype',lazy='dynamic')
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
        return '<Product Type {}>'.format(self.name)
    
    def setName(self, name):
        self.name = name
    
    def setDescription(self, description):
        self.description = description
    
    
def getAll():
    return ProductType.query.all()

def getById(product_type_id):
    return ProductType.query.filter_by(id=product_type_id).first()

def getByName(name):
    return ProductType.query.filter_by(name=name).first()