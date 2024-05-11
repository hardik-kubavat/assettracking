from sqlalchemy.sql.expression import asc
from project import db,logger
from sqlalchemy import event,desc
from datetime import datetime
from project.models.ProductModel import Product


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "product.id"), nullable=False)
    locater_id = db.Column(db.Integer, db.ForeignKey(
        "locater.id"), nullable=False)
    remarks = db.Column(db.String(), nullable=True)
    created_at = db.Column(
        db.TIMESTAMP(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(), default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)
    associatetransaction_id = db.Column(
        db.Integer, db.ForeignKey("transaction.id"), nullable=True)

    def __init__(self, product_id, locater_id, remarks=None):
        self.product_id = product_id
        self.locater_id = locater_id
        self.remarks = remarks
        

    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'product_id': self.product_id,
            'locater_id': self.locater_id,
            'srno': self.product.srno,
            'identification': self.product.identification,
            'locater': self.locater.name,
            'remarks': self.remarks,
            'product_type':self.product.producttype.name,
            'category':self.product.category.name,
            'createdat':str(self.created_at)
        }

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

#Bind adter insert event
@event.listens_for(Transaction,"after_insert")
def update_locater_in_product(mapper, connection, target):
    logger.debug("In After insert method... enjoy")
    logger.debug("Target Product ID : {}".format(target.product_id))
    logger.debug("Target Locater ID : {}".format(target.locater_id))
    product = Product.__table__
    connection.execute(product.update().where(Product.id==target.product_id).values(currentlocater_id=target.locater_id))
    
def getAll():
    return Transaction.query.order_by(asc(Transaction.created_at)).all()

def getByProductId(product_id):
    return Transaction.query.filter_by(product_id=product_id).order_by(desc(Transaction.created_at)).all()