from flask import render_template,Blueprint,make_response

from project.models import ProductTypeModel,CategoryModel,LocaterModel,ProductModel
from project.extention import db

nav = Blueprint("navigation",__name__, url_prefix="/")

################## Navigations routes ##################
@nav.route('/')
def index():
    hq_ptype_dash_data = dict()
    for p in ProductTypeModel.getAll():
        hq_ptype_dash_data[p.name] = ProductModel.getProductTypeDashboardHQ(p.id)
    print(hq_ptype_dash_data) 
    return render_template('dashboard.html', desktop_data = ProductModel.getDesktopDashboardHQ(), printer_data = ProductModel.getPrinterDashboardHQ(), monitor_data = ProductModel.getMonitorDashboardHQ(), hq_ptype_dash_data=hq_ptype_dash_data)


@nav.route('/category')
def category():
    return render_template('category_new.html',producttypes=ProductTypeModel.getAll())

#TOBEREMOVED
@nav.route('/product')
def product():
    return render_template('asset.html',producttypes=ProductTypeModel.getAll(),categories=CategoryModel.getAll(),locaters=LocaterModel.getAll())

@nav.route('/asset')
def asset():
    return render_template('asset.html',producttypes=ProductTypeModel.getAll(),categories=CategoryModel.getAll(),locaters=LocaterModel.getAll())


@nav.route('/locater')
def locater():
    return render_template('locater_new.html')

@nav.route('/user')
def user():
    return render_template('user.html')

@nav.route('/allocation')
def allocation():
    return render_template('allocation.html')

@nav.route('/search')
def search():
    return render_template('index.html')

@nav.route('/reports')
def reports():
    return render_template('reports.html')

@nav.route('/producttype')
def producttype():
    return render_template('producttype_new.html')

@nav.route('/servicecall')
def servicecall():
    return render_template('servicecall.html')

@nav.route('/createdb')
def createdb():
    try:
        db.create_all()
        db.session.commit()
    except:
        print("Error in creating database")
        return make_response("500")
    return make_response("200")