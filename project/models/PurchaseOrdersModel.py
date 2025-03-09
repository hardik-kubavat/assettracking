from project.extention import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_order'

    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(), nullable=False, unique=True)
    po_title = db.Column(db.String(), nullable=False)
    po_date = db.Column(db.Date, nullable=False)
    delivery_date = db.Column(db.Date, nullable=True)
    warranty_ends = db.Column(db.Date, nullable=True)
    deadstock_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.String(), nullable=True)
    isdeleted = db.Column(db.Boolean, default=False, nullable=False)
    po_file = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.TIMESTAMP(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'po_number': self.po_number,
            'po_title' : self.po_title,
            'po_date': self.po_date.strftime("%d-%m-%Y"),
            'delivery_date': self.delivery_date.strftime("%d-%m-%Y") if self.delivery_date else None,
            'warranty_ends': self.warranty_ends.strftime("%d-%m-%Y") if self.warranty_ends else None,
            'deadstock_date': self.deadstock_date.strftime("%d-%m-%Y") if self.deadstock_date else None,
            'description': self.description,
            'po_file': self.po_file,
            'isdeleted': self.isdeleted,
        }

    def __init__(self, po_number, po_title, po_date, delivery_date=None, warranty_ends=None, description=None, isdeleted=False, po_file=None, deadstock_date=None):
        self.po_number = po_number
        self.po_date = po_date
        self.delivery_date = delivery_date
        self.warranty_ends = warranty_ends
        self.description = description
        self.isdeleted = isdeleted
        self.po_file = po_file
        self.po_title = po_title
        self.deadstock_date = deadstock_date

    def __repr__(self):
        return '<Purchase Order {}>'.format(self.po_number)
    
    def setPoFile(self, po_file):
        self.po_file = po_file


    # Function to save the uploaded file
    def save_po_file(po_file):
        upload_folder = 'static/uploads/po_files'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Use secure_filename to ensure the file name is safe
        filename = secure_filename(po_file.filename)
        file_path = os.path.join(upload_folder, filename)
        po_file.save(file_path)
        return filename

    def setPoNumber(self, po_number):
        self.po_number = po_number

    def setPoDate(self, po_date):
        self.po_date = po_date

    def setDeliveryDate(self, delivery_date):
        self.delivery_date = delivery_date

    def setWarrantyEnds(self, warranty_ends):
        self.warranty_ends = warranty_ends

    def setDeadstockDate(self, deadstock_date):
        self.deadstock_date = deadstock_date

    def setDescription(self, description):
        self.description = description
    
    def setPoTitle(self, title):
        self.po_title = title


# Getter functions for Purchase Order

def getAll():
    return PurchaseOrder.query.filter_by(isdeleted=False).all()

def getById(po_id):
    return PurchaseOrder.query.filter_by(id=po_id).first()

def getByPoNumber(po_number):
    return PurchaseOrder.query.filter_by(po_number=po_number).first()
