from sqlalchemy.sql.expression import desc
from project.extention import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

#Models
from . import ProductTypeModel

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    description = db.Column(db.String(),nullable=True)
    product_type_id = db.Column(db.Integer,db.ForeignKey('product_type.id'),nullable=False)
    products = db.relationship('Product',backref='category',lazy='dynamic')
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
            'product_type':self.producttype.name,
            'product_type_id': self.producttype.id 
        }
    
    def __init__(self, name,description,product_type_id,isdeleted=False):
        self.name = name
        self.description = description
        self.isdeleted = isdeleted
        self.product_type_id = product_type_id

    def __repr__(self):
        return '<Category {}>'.format(self.name)
    
    def setName(self, name):
        self.name = name
    
    def setDescription(self, description):
        self.description = description
    
    def setProductTypeID(self, product_type_id):
        self.product_type_id = product_type_id
        
def getAll():
    return Category.query.order_by(desc(Category.name)).all()

def getById(category_id):
    return Category.query.filter_by(id=category_id).first()

def getByName(name):
    return Category.query.filter_by(name=name).first()

def getByNameAndProductType(name,product_type_id):
    return Category.query.filter_by(name=name,product_type_id=product_type_id).first()