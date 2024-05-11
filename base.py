import os,traceback,sys

from flask import Flask, render_template,make_response
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
import logging
from project import db, app


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


