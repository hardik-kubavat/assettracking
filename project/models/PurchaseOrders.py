from project.extention import db
from datetime import datetime

class PurchaseOrders(db.Model):
    __tablename__ = 'purchase_orders'

    id = db.Column(db.Integer, primary_key=True)
    po_no = db.Column(db.String(), unique=True, nullable=False)
    title = db.Column(db.String(), unique=True, nullable=False)
    po_date = db.Column(db.TIMESTAMP(), default=datetime.now(), nullable=False)
    warranty_up_to = db.Column(db.TIMESTAMP(), default=datetime.now(), nullable=False)
    remarks = db.Column(db.String(), nullable=True)
    received_date = db.Column(db.TIMESTAMP(), default=datetime.now(), nullable=False)
    filename = db.Column(db.String(), unique=True, nullable=False)
