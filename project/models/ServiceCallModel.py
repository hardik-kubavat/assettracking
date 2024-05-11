from project import db,logger
from constants import Owner, Status
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import event,desc
from datetime import datetime
from project.models.ProductModel import Product


class ServiceCall(db.Model):
    __tablename__ = 'servicecall'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "product.id"), nullable=False)
    status = db.Column(db.String(), nullable=True)
    ticket_id = db.Column(db.String(), nullable=False)
    service_id = db.Column(db.String(), nullable=True)
    description = db.Column(db.String(), nullable=False)
    replaced_item = db.Column(db.String(), nullable=True)
    call_log_date = db.Column(
        db.TIMESTAMP(), default=datetime.utcnow, nullable=False)
    call_close_date = db.Column(
        db.TIMESTAMP(), nullable=True)
    
    created_at = db.Column(
        db.TIMESTAMP(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(), default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    def __init__(self, product_id,ticket_id,service_id,description,call_log_date,status="P"):
        self.product_id = product_id
        self.status = status
        self.ticket_id = ticket_id
        self.service_id = service_id
        self.description = description
        self.call_log_date = call_log_date
        

    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'product_id': self.product_id,
            'srno': self.product.srno,
            'identification': self.product.identification,
            'ticket_id': self.ticket_id,
            'service_order_id': self.service_id,
            'description':self.description,
            'replace_item':self.replaced_item,
            'created_at':str(self.created_at)
        }

    def __repr__(self):
        return '<ServiceCall {}>'.format(self.id)
    
    def setProductId(self, product_id):
        self.product_id = product_id
        
    def setStatus(self, status):
        self.status = status
        
    def setTicketId(self, ticket_id):
        self.ticket_id = ticket_id
    
    def setServiceId(self, service_id):
        self.service_id = service_id
    
    def setDescription(self, desc):
        self.description = desc
    
    def setReplacedItem(self, replaced_item):
        self.replaced_item = replaced_item
        
    def setCallLogDate(self,call_log_date):
        self.call_log_date = call_log_date
    
    def setCallCloseDate(self,call_close_date):
        self.call_close_date = call_close_date
    
    

    
def getAll():
    return ServiceCall.query.all()

