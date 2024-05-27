from sqlalchemy.sql.expression import desc
from project.extention import db
from constants import Status
from datetime import datetime
from sqlalchemy.sql import text
from project import logger
import os
# Models
from . import ProductTypeModel,CategoryModel


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    product_type_id = db.Column(db.Integer, db.ForeignKey(
        "product_type.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        "category.id"), nullable=False)
    srno = db.Column(db.String(), unique=True, nullable=False)
    identification = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(2), nullable=False,
                       server_default=str(Status.WORKING))
    owner = db.Column(db.String(2), nullable=False)
    remarks = db.Column(db.String(), nullable=True)
    currentlocater_id = db.Column(
        db.Integer, db.ForeignKey("locater.id"), nullable=True)
    created_at = db.Column(
        db.TIMESTAMP(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(), default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)
    transactions = db.relationship('Transaction',backref='product',cascade="all, delete-orphan",lazy='dynamic')
    
    

    def __init__(self, product_type_id, category_id, srno, identification, status, owner, remarks=None, currentlocater_id=None):
        self.product_type_id = product_type_id
        self.category_id = category_id
        self.srno = srno
        self.identification = identification
        self.status = status
        self.owner = owner
        self.remarks = remarks
        self.currentlocater_id = currentlocater_id

    @property
    def serialize(self):
        status = 'Working'
        if self.status != 'WO':
            status = 'Not Working'

        if self.owner == 'HC':
            owner = 'High Court'
        elif self.owner == 'EC':
            owner = 'E-Commitee'
        elif self.owner == 'CC':
            owner = 'Civil Court'
        else:
            owner = 'District Court'
        return {
            'id': str(self.id),
            'product_type_id': self.producttype.id,
            'producttype': self.producttype.name,
            'category_id': self.category.id,
            'category': self.category.name,
            'srno': self.srno,
            'identification': self.identification,
            'status': self.status,
            'statustext': status,
            'owner': self.owner,
            'ownertext': owner,
            'remarks': self.remarks,
            'currentlocater_id': 0 if self.currentlocater_id == None else self.currentlocater_id,
            'currentlocation': "" if self.currentlocater_id == None else self.locater.name
        }

    def __repr__(self):
        return '<Product {}>'.format(self.srno)

    def setProductTypeID(self, product_type_id):
        self.product_type_id = product_type_id

    def setCategoryID(self, category_id):
        self.category_id = category_id

    def setSrno(self, srno):
        self.srno = srno

    def setIdentification(self, identification):
        self.identification = identification

    def setStatus(self, status):
        self.status = status

    def setOwner(self, owner):
        self.owner = owner

    def setRemarks(self, remarks):
        self.remarks = remarks

    def setCurrentLocaterID(self, locater_id):
        self.currentlocater_id = locater_id
    
def getSuggestions(term):
    result = db.session.execute(text("SELECT identification from product where identification like '%"+term+"%' UNION SELECT srno from product where srno like '%"+term+"%' LIMIT 10")).fetchall()
    suggestions = []
    if len(result) == 0:
        suggestions.append("No Result")
    else:
        for row in result:
            suggestions.append(row[0])
    return suggestions

def getById(product_id):
    return Product.query.filter_by(id=product_id).first()

def getBySrnoOrIdentification(query):
    return Product.query.filter((Product.srno == query) | (Product.identification == query)).first()

def getNotWorkingProducts():
    return Product.query.filter(Product.status == 'NW').order_by(desc(Product.category_id)).all()

def getSummeryByCategory(query):
    return db.session.query(CategoryModel.Category.name,db.func.count(Product.srno)).join(ProductTypeModel.ProductType,Product.product_type_id==ProductTypeModel.ProductType.id).join(CategoryModel.Category,Product.category_id==CategoryModel.Category.id).group_by(CategoryModel.Category.name).all()

def getDesktopDashboardHQ():
    query = "SELECT name,sum(working) as working ,sum(not_working) as not_working,sum(ewaste) as ewaste FROM (SELECT c.name, CASE WHEN p.status =  'WO' THEN count(*) ELSE 0 END as working, CASE WHEN p.status='NW' THEN count(*) ELSE 0 END as not_working,CASE WHEN p.status =  'EW' THEN count(*) ELSE 0 END as ewaste FROM product p INNER JOIN category c ON c.id = p.category_id INNER JOIN locater l ON l.id = p.currentlocater_id INNER JOIN product_type pt on pt.id = p.product_type_id WHERE l.name in ("+os.getenv('D1_LOCATER')+") and l.ishq='true' and pt.name='"+os.getenv('D1_DESKTOP_PRODUCT_TYPE_NAME')+"' group by c.name, p.status) as inner_query GROUP BY name"
    logger.info("Desktop Dashboard Query : %s" % (query))
    result = db.session.execute(text(query)).fetchall()
    return result

def getPrinterDashboardHQ():
    query = "SELECT name,sum(working) as working ,sum(not_working) as not_working,sum(ewaste) as ewaste FROM (SELECT c.name, CASE WHEN p.status =  'WO' THEN count(*) ELSE 0 END as working, CASE WHEN p.status='NW' THEN count(*) ELSE 0 END as not_working,CASE WHEN p.status =  'EW' THEN count(*) ELSE 0 END as ewaste FROM product p INNER JOIN category c ON c.id = p.category_id INNER JOIN locater l ON l.id = p.currentlocater_id INNER JOIN product_type pt on pt.id = p.product_type_id WHERE l.name in ("+os.getenv('D1_LOCATER')+") and l.ishq='true' and pt.name='"+os.getenv('D1_PRINTER_PRODUCT_TYPE_NAME')+"' group by c.name, p.status) as inner_query GROUP BY name"
    logger.info("Printer Dashboard Query : %s" % (query))
    result = db.session.execute(text(query)).fetchall()
    return result
    
def getMonitorDashboardHQ():
    query = "SELECT name,sum(working) as working ,sum(not_working) as not_working,sum(ewaste) as ewaste FROM (SELECT c.name, CASE WHEN p.status =  'WO' THEN count(*) ELSE 0 END as working, CASE WHEN p.status='NW' THEN count(*) ELSE 0 END as not_working,CASE WHEN p.status =  'EW' THEN count(*) ELSE 0 END as ewaste FROM product p INNER JOIN category c ON c.id = p.category_id INNER JOIN locater l ON l.id = p.currentlocater_id INNER JOIN product_type pt on pt.id = p.product_type_id WHERE l.name in ("+os.getenv('D1_LOCATER')+") and l.ishq='true' and pt.name='"+os.getenv('D1_MONITOR_PRODUCT_TYPE_NAME')+"' group by c.name, p.status) as inner_query GROUP BY name"
    logger.info("Monitor Dashboard Query : %s" % (query))
    result = db.session.execute(text(query)).fetchall()
    return result

def getProductTypeDashboardHQ(product_type_id):
    query = "SELECT name,sum(working) as working ,sum(not_working) as not_working,sum(ewaste) as ewaste FROM (SELECT c.name, CASE WHEN p.status =  'WO' THEN count(*) ELSE 0 END as working, CASE WHEN p.status='NW' THEN count(*) ELSE 0 END as not_working,CASE WHEN p.status =  'EW' THEN count(*) ELSE 0 END as ewaste FROM product p INNER JOIN category c ON c.id = p.category_id INNER JOIN locater l ON l.id = p.currentlocater_id INNER JOIN product_type pt on pt.id = p.product_type_id WHERE  l.ishq='true' and pt.id="+str(product_type_id)+" group by c.name, p.status) as inner_query GROUP BY name"
    logger.info("Product Type Dashboard Query : %s" % (query))
    result = db.session.execute(text(query)).fetchall()
    return result