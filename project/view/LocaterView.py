from flask import Blueprint,request, make_response, jsonify,redirect,url_for
from project.models.LocaterModel import Locater
from project import logger
from project.extention import db


lv = Blueprint('locater','locater',url_prefix="/locater")

@lv.route('/add',methods=['GET','POST'])
def addorupdate():
    if request.form and request.form.get('locater_id') == '':
        ishq = True if request.form.get('ishq') else False
        logger.debug("Locater add operation is executing...")
        try:
            locater = Locater(name=request.form.get('name'),description=request.form.get('description'),ishq=ishq)
            db.session.add(locater)
            db.session.commit()
            logger.debug("Lcoater added successfully. {0} {1}".format(locater.id,request.form.get("name")))
            return make_response("success"),200
        except Exception as e:
            logger.error(str(e))
            return make_response(str(e)),500
    else:
        logger.debug("Locater {} - Update operation is executing... ".format(request.form.get('locater_id')))
        ishq = True if request.form.get('ishq') else False
        try:
            locater = Locater.query.filter_by(id=request.form.get('locater_id')).first()
            locater.setName(request.form.get('name'))
            locater.setDescription(request.form.get('description'))
            locater.ishq = ishq
            db.session.commit()
            logger.debug("Locater {} - Updated successfully...".format(request.form.get('locater_id')))
            return make_response("success"),200
        except Exception as e:
            logger.debug(str(e))
            return make_response(str(e)),500
    logger.debug("Add/Update data request is not recevied as form. Please Troubleshoot")
    return make_response("There is an error... Please check logs"),500

@lv.route('/delete/<locater_id>')
def delete(locater_id):
    logger.debug("Locater {} - Delete operation is executing. ".format(locater_id))
    locater = Locater.query.filter_by(id=locater_id).first()
    db.session.delete(locater)
    db.session.commit()
    logger.debug("Locater {} - Deleted Successfully.")
    return redirect(url_for("navigation.locater"))

@lv.route('/get/<locater_id>',methods=['GET'])
def get_locater_by_id(locater_id):
    return jsonify(Locater.query.filter_by(id=locater_id).first().serialize)

@lv.route('/get_data')
def get_all_locaters():
    return jsonify(data = [ i.serialize for i in Locater.query.all()])

