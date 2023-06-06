import os,traceback,sys

from flask import Flask, render_template,make_response
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
import logging


#Initialize app
app = Flask(__name__, instance_relative_config=True)

################### Logger ###########################
logging.basicConfig(level=logging.DEBUG)
assettracking_handler = logging.FileHandler(filename="/var/log/assettracking.log")
app.logger.setLevel(logging.DEBUG)
app.logger.removeHandler(default_handler)
app.logger.addHandler(assettracking_handler)
logger = app.logger
logger.info("Application has been initialized....")
######################################################

#Provided application configuration through config.py file.
app.config.from_object(DevelopmentConfig)


try:
    os.makedirs(app.instance_path)
except:
    pass

################ Initialize database ######################
db = SQLAlchemy(app)
###########################################################

############## Database Models(Tables) #####################
from models import UserModel
from models import LocaterModel
from models import CategoryModel
from models import ProductTypeModel
from models import ProductModel
from models import TransactionModel
from models import ServiceCallModel
############################################################

############### Register Blueprints ####################
#NavigationView
from view.NavigationView import nav
app.register_blueprint(nav)
#Userview
from view.UserView import uv
app.register_blueprint(uv)
#Locaterview
from view.LocaterView import lv
app.register_blueprint(lv)
#ProductTypeView
from view.ProductTypeView import pv
app.register_blueprint(pv)
#CategoryView
from view.CategoryView import cv
app.register_blueprint(cv)
#ProductView
from view.ProductView import pv
app.register_blueprint(pv)
#Trascation/Allocation view
from view.TransactionView import tv
app.register_blueprint(tv)
#Trascation/Allocation view
from view.ReportView import rv
app.register_blueprint(rv)
from view.ServiceCallView import sv
app.register_blueprint(sv)
################### Blueprints #########################



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


