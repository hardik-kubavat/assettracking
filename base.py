import os,traceback,sys

from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from project.extention import db
from project import logger


##################### Routes #########################
@app.route('/createdb')
def createdb():
    try:
        db.create_all()
        db.session.commit()
    except:
        print("Error in creating database")
        traceback.print_exc(file=sys.stdout)
        return make_response("500")
    return make_response("200")
######################################################

################ DASHBOARD CONFIGURATION #############
######################################################


