from flask import Blueprint,request,render_template, make_response, jsonify,redirect,url_for,send_file
from project.models.ProductModel import Product
from project import db,logger
from import_products import import_products
from project.models import ProductModel
import os

pv = Blueprint('product','product',url_prefix="/product")

@pv.route('/add',methods=['GET','POST'])
def addorupdate():
    if request.form and request.form.get('product_id') == '':
        logger.debug("Product add operation is executing...")
        logger.debug(str(request.form))
        try:
            product = Product(product_type_id=request.form.get('producttype'),category_id=request.form.get('category'),srno=request.form.get('srno'),identification=request.form.get('identification'),status=request.form.get('status'),owner=request.form.get('owner'),remarks=request.form.get('remarks'))
            db.session.add(product)
            db.session.commit()
            logger.debug("Product added successfully. {0} ".format(product.id))
            return make_response("success"),200
        except Exception as e:
            logger.error(str(e))
            return make_response(str(e)),500
    else:
        logger.debug("Product {} - Update operation is executing... ".format(request.form.get('product_id')))
        try:
            product = Product.query.filter_by(id=request.form.get('product_id')).first()
            product.setProductTypeID(request.form.get('producttype'))
            product.setCategoryID(request.form.get('category'))
            product.setSrno(request.form.get('srno'))
            product.setIdentification(request.form.get('identification'))
            product.setStatus(request.form.get('status'))
            product.setOwner(request.form.get('owner'))
            product.setRemarks(request.form.get('remarks'))
            db.session.commit()
            logger.debug("Product {} - Updated successfully...".format(request.form.get('product_id')))
            return make_response("success"),200
        except Exception as e:
            logger.debug(str(e))
            return make_response(str(e)),500
    logger.debug("Add/Update data request is not recevied as form. Please Troubleshoot")
    return make_response("There is an error... Please check logs"),500

@pv.route('/<product_id>',methods=['DELETE'])
def delete(product_id):
    logger.debug("Product {} - Delete operation is executing. ".format(product_id))
    product = Product.query.filter_by(id=product_id).first()
    db.session.delete(product)
    db.session.commit()
    logger.debug("Product {} - Deleted Successfully.")
    return redirect(url_for("navigation.product"),200)

@pv.route('/<product_id>',methods=['GET'])
def get_product_by_id(product_id):
    return jsonify(Product.query.filter_by(id=product_id).first().serialize)

@pv.route('/',methods=['POST'],strict_slashes=False)
def upload_bulk_products():
    logger.debug("In Products Upload")
    if request.method == 'POST':
        file = request.files['products']
        logger.debug("File Name is {} ".format(file.filename))
        import_products(file)
        return send_file(os.path.join(app.root_path, 'logs', file.filename),as_attachment=True)
    return redirect(url_for("navigation.product"),302)

@pv.route('/',methods=["GET"])
def get_all_products():
    return jsonify(data = [ i.serialize for i in Product.query.all()])

@pv.route('/autocomplete',methods=["GET"])
def get_suggestions():
    term=request.args.get("term")
    return jsonify(ProductModel.getSuggestions(term))

@pv.route('/find/<query>')
def get_by_srno_or_identification(query):
    return jsonify(ProductModel.getBySrnoOrIdentification(query).serialize)




