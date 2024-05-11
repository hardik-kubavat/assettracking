from flask import Blueprint,request,render_template, make_response, jsonify,redirect,url_for
from project.models.CategoryModel import Category
from project import db,logger
import traceback

cv = Blueprint('category','category',url_prefix="/category")

@cv.route('/add',methods=['GET','POST'])
def addorupdate():
    if request.form and request.form.get('category_id') == '':
        logger.debug("Category add operation is executing...")
        logger.debug(str(request.form))
        try:
            category = Category(name=request.form.get('name'),description=request.form.get('description'),product_type_id=request.form.get('producttype'))
            db.session.add(category)
            db.session.commit()
            logger.debug("Category added successfully. {0} {1}".format(category.id,request.form.get("name")))
            return make_response("success"),200
        except Exception as e:
            logger.error(str(e))
            return make_response(str(e)),500
    else:
        logger.debug("Category {} - Update operation is executing... ".format(request.form.get('category_id')))
        try:
            category = Category.query.filter_by(id=request.form.get('category_id')).first()
            category.setName(request.form.get('name'))
            category.setDescription(request.form.get('description'))
            category.setProductTypeID(request.form.get('producttype'))
            db.session.commit()
            logger.debug("category {} - Updated successfully...".format(request.form.get('category_id')))
            return make_response("success"),200
        except Exception as e:
            logger.debug(str(e))
            return make_response(str(e)),500
    logger.debug("Add/Update data request is not recevied as form. Please Troubleshoot")
    return make_response("There is an error... Please check logs"),500

@cv.route('/delete/<category_id>')
def delete(category_id):
    logger.debug("category {} - Delete operation is executing. ".format(category_id))
    category = Category.query.filter_by(id=category_id).first()
    db.session.delete(category)
    db.session.commit()
    logger.debug("category {} - Deleted Successfully.")
    return redirect(url_for("navigation.category"))

@cv.route('/get/<category_id>',methods=['GET'])
def get_category_by_id(category_id):
    return jsonify(Category.query.filter_by(id=category_id).first().serialize)

@cv.route('/get_data')
def get_all_category():
    return jsonify(data = [ i.serialize for i in Category.query.all()])

