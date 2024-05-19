from project.extention import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_utils import PasswordType
from datetime import datetime

#Users
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(),nullable=False)
    lastname = db.Column(db.String(),nullable=False)
    emailid = db.Column(db.String(),unique=True,nullable=False)
    mobile = db.Column(db.Numeric())
    isdeleted = db.Column(db.Boolean(create_constraint=True, name="isdeletedcheck"))
    created_at = db.Column(db.TIMESTAMP(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    password = db.Column(PasswordType(64,schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ]))
    
    @property
    def serialize(self):
        return {
            'id' : str(self.id),
            'firstname':self.firstname,
            'lastname':self.lastname,
            'emailid':self.emailid,
            'mobile':str(self.mobile),
            'isdeleted':self.isdeleted,
        }
    
    def __init__(self, firstname,lastname,emailid=None,mobile=None,password="abc123",isdeleted=False):
        self.firstname = firstname
        self.lastname = lastname
        self.emailid = emailid
        self.mobile = None if mobile == '' else mobile 
        self.password = password
        self.isdeleted = isdeleted

    def __repr__(self):
        return '<User {}>'.format(self.emailid)
    
    def setFirstName(self, firstname):
        self.firstname = firstname
    
    def setLastName(self, lastname):
        self.lastname = lastname
    
    def setEmailid(self, emailid):
        self.emailid = emailid
    
    def setPassword(self, password):
        self.password = password
    
    def setMobile(self, mobile):
        self.mobile = mobile
    