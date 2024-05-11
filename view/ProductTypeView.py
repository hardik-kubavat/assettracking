from flask import Blueprint,request,render_template, make_response, jsonify,redirect,url_for
from project.models.ProductTypeModel import *
from project import db,logger
import traceback

pv = Blueprint('ProductType','Producttype',url_prefix="/producttype")

@pv.route('/add',methods=['GET','POST'])
def addorupdate():
    if request.form and request.form.get('product_type_id') is '':
        logger.debug("Product Type add operation is executing...")
        try:
            product_type = ProductType(name=request.form.get('name'),description=request.form.get('description'))
            db.session.add(product_type)
            db.session.commit()
            logger.debug("Product Type added successfully. {0} {1}".format(product_type.id,request.form.get("name")))
            return make_response("success"),200
        except Exception as e:
            logger.error(str(e))
            return make_response(str(e)),500
    else:
        logger.debug("Product Type {} - Update operation is executing... ".format(request.form.get('product_type_id')))
        try:
            product_type = ProductType.query.filter_by(id=request.form.get('product_type_id')).first()
            product_type.setName(request.form.get('name'))
            product_type.setDescription(request.form.get('description'))
            db.session.commit()
            logger.debug("Product Type {} - Updated successfully...".format(request.form.get('product_type_id')))
            return make_response("success"),200
        except Exception as e:
            logger.debug(str(e))
            return make_response(str(e)),500
    logger.debug("Add/Update data request is not recevied as form. Please Troubleshoot")
    return make_response("There is an error... Please check logs"),500

@pv.route('/delete/<product_type_id>')
def delete(product_type_id):
    logger.debug("Product Type {} - Delete operation is executing. ".format(product_type_id))
    #product_type = ProductType.query.filter_by(id=product_type_id).first()
    product_type = getById(product_type_id)
    db.session.delete(product_type)
    db.session.commit()
    logger.debug("Product Type {} - Deleted Successfully.")
    return redirect(url_for("navigation.producttype"))

@pv.route('/get/<product_type_id>',methods=['GET'])
def get_producttype_by_id(product_type_id):
    return jsonify(getById(product_type_id).serialize)

@pv.route('/get_data')
def get_all_producttype():
    return jsonify(data = [ i.serialize for i in getAll()])

@pv.route('/<product_type_id>/categories',methods=['GET'])
def get_categories_by_product_type(product_type_id):
    return jsonify([ i.serialize for i in getById(product_type_id).categories])