import os,sys

from flask import Flask, render_template,make_response
from flask.logging import default_handler
import logging
sys.path.append('/home/hlkubavat/apps/assettracking/venv/lib/python3.8/site-packages')
sys.path.append('/home/hlkubavat/apps/assettracking')
from config import DevelopmentConfig
from project.extention import db
from dotenv import load_dotenv
load_dotenv()
print("Loading Environments done")
logging.basicConfig(filename=os.getenv("APP_LOG_PATH"), level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    #Initialize app
    app = Flask(__name__, instance_relative_config=True)

    ################### Logger ###########################
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

    ############### Register Blueprints ####################
    #NavigationView
    from project.view.NavigationView import nav
    app.register_blueprint(nav)
    logger.info("Navigation view initialized")
    #Userview
    from project.view.UserView import uv
    app.register_blueprint(uv)
    #Locaterview
    from project.view.LocaterView import lv
    app.register_blueprint(lv)
    #ProductTypeView
    from project.view.ProductTypeView import pv
    app.register_blueprint(pv)
    #CategoryView
    from project.view.CategoryView import cv
    app.register_blueprint(cv)
    #ProductView
    from project.view.ProductView import pv
    app.register_blueprint(pv)
    #Trascation/Allocation view
    from project.view.TransactionView import tv
    app.register_blueprint(tv)
    #Trascation/Allocation view
    from project.view.ReportView import rv
    app.register_blueprint(rv)
    from project.view.ServiceCallView import sv
    app.register_blueprint(sv)
    from project.view.FileView import comv
    app.register_blueprint(comv)
    ################### Blueprints #########################

    return app

if __name__ == "__main__":
    create_app.run()
