import os,traceback,sys

from flask import Flask, render_template,make_response
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
import logging
sys.path.append('/home/hlkubavat/apps/assettracking/venv/lib/python3.8/site-packages')
sys.path.append('/home/hlkubavat/apps/assettracking')
from config import DevelopmentConfig

db = SQLAlchemy()
logger = None

def create_app():
    #Initialize app
    app = Flask(__name__, instance_relative_config=True)

    ################### Logger ###########################
    logging.basicConfig(level=logging.DEBUG)
    assettracking_handler = logging.FileHandler(filename="/var/www/assettracking/logs/assettracking.log")
    app.logger.setLevel(logging.DEBUG)
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(assettracking_handler)
    logger = app.logger
    logger.info("Application has been initialized....")
    ######################################################

    #Provided application configuration through config.py file.
    app.config.from_object(DevelopmentConfig)    
    #Initialized Database
    db.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except:
        pass

    ############## Database Models(Tables) #####################
    from project.models import UserModel
    from project.models import LocaterModel
    from project.models import CategoryModel
    from project.models import ProductTypeModel
    from project.models import ProductModel
    from project.models import TransactionModel
    from project.models import ServiceCallModel
    ############################################################

    ############### Register Blueprints ####################
    #NavigationView
    from view.NavigationView import nav
    app.register_blueprint(nav)
    logger.info("Navigation view initialized")
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
    from view.FileView import comv
    app.register_blueprint(comv)
    ################### Blueprints #########################

    return app
