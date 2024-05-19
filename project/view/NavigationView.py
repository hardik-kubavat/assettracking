from flask import render_template,Blueprint

from project.models import ProductTypeModel,CategoryModel,LocaterModel

nav = Blueprint("navigation",__name__, url_prefix="/")

################## Navigations routes ##################
@nav.route('/')
def index():
    return render_template('index.html')


@nav.route('/category')
def category():
    return render_template('category.html',producttypes=ProductTypeModel.getAll())


@nav.route('/product')
def product():
    return render_template('product.html',producttypes=ProductTypeModel.getAll(),categories=CategoryModel.getAll(),locaters=LocaterModel.getAll())


@nav.route('/locater')
def locater():
    return render_template('locater.html')

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
    return render_template('producttype.html')

@nav.route('/servicecall')
def servicecall():
    return render_template('servicecall.html')