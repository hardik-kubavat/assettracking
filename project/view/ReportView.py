from flask import Blueprint,request,render_template, make_response, jsonify,redirect,url_for
from flask_weasyprint import HTML,render_pdf
from project import logger
from project.models import LocaterModel,ProductTypeModel,CategoryModel,ProductModel
import time

rv = Blueprint('report','report',url_prefix="/report")

@rv.route('/locaterwise',methods=['GET'])
def generate_locater_wise_report():
    html = render_template("rpt_locaterreport.html",locaters = LocaterModel.getAll())
    return render_pdf(HTML(string=html),download_filename="Locaterwise_"+time.strftime("%Y%m%d-%H%M%S"))

@rv.route('/producttypewise',methods=['GET'])
def generate_producttype_wise_report():
    html = render_template("rpt_producttypereport.html",producttypes = ProductTypeModel.getAll())
    return render_pdf(HTML(string=html),download_filename="Producttypewise_"+time.strftime("%Y%m%d-%H%M%S"))

@rv.route('/categorywise',methods=['GET'])
def generate_category_wise_report():
    html = render_template("rpt_categoryreport.html",categories = CategoryModel.getAll())
    return render_pdf(HTML(string=html),download_filename="Categorywise_"+time.strftime("%Y%m%d-%H%M%S"))

@rv.route('/notworkingasset',methods=['GET'])
def generate_notworking_asset_report():
    html = render_template("rpt_notworkingproducts.html",products = ProductModel.getNotWorkingProducts())
    return render_pdf(HTML(string=html),download_filename="NotworkingAsset_"+time.strftime("%Y%m%d-%H%M%S"))

@rv.route('/dashboard',methods=['GET'])
def generate_dashboard():
    logger.debug(str(ProductModel.getSummeryByCategory(None)))
    return ProductModel.getSummeryByCategory(None)
