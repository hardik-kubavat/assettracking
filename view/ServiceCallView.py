from flask import Blueprint,request,render_template, make_response, jsonify,redirect,url_for,send_file
from models.ServiceCallModel import ServiceCall
from base import app,db,logger
from import_products import import_products
import traceback
import time,os

sv = Blueprint('servicecall','servicecall',url_prefix="/servicecalls")

@sv.route('/add',methods=['GET','POST'])
def addorupdate():
    if request.form and request.form.get('servicecall_id') is '':
        logger.info("Service Call add operation is executing...")
        logger.debug(str(request.form))
        try:
            serviceCall = ServiceCall(request.form.get('product_id'),request.form.get('ticket_id'),request.form.get('service_id'),request.form.get('description'),request.form.get('call_log_date'),request.form.get('status'))
            db.session.add(serviceCall)
            db.session.commit()
            logger.debug("Service Call added successfully. {0} ".format(serviceCall.id))
            return make_response("success"),200
        except Exception as e:
            logger.error(str(e))
            return make_response(str(e)),500
    else:
        logger.debug("Service Call {} - Update operation is executing... ".format(request.form.get('servicecall_id')))
        try:
            serviceCall = ServiceCall.query.filter_by(id=request.form.get('servicecall_id')).first()
            serviceCall.setProductId(request.form.get("product_id"))
            serviceCall.setStatus(request.form.get('status'))
            serviceCall.setTicketId(request.form.get('ticket_id'))
            serviceCall.setServiceId(request.form.get('service_id'))
            serviceCall.setDescription(request.form.get('description'))
            serviceCall.setReplacedItem(request.form.get('replaced_item'))
            serviceCall.setCallLogDate(request.form.get('call_log_date'))
            serviceCall.setCallCloseDate(request.form.get('call_close_date'))
            db.session.commit()
            logger.debug("Service Call {} - Updated successfully...".format(request.form.get('servicecall_id')))
            return make_response("success"),200
        except Exception as e:
            logger.debug(str(e))
            return make_response(str(e)),500
    logger.debug("Add/Update data request is not recevied as form. Please Troubleshoot")
    return make_response("There is an error... Please check logs"),500

@sv.route('/<serviceall_id>',methods=['DELETE'])
def delete(servicecall_id):
    logger.debug("Service Call {} - Delete operation is executing. ".format(servicecall_id))
    serviceCall = ServiceCall.query.filter_by(id=servicecall_id).first()
    db.session.delete(serviceCall)
    db.session.commit()
    logger.debug("Service Call {} - Deleted Successfully.")
    return redirect(url_for("navigation.servicecall"),200)

@sv.route('/<servicecall_id>',methods=['GET'])
def get_servicecall_by_id(servicecall_id):
    return jsonify(ServiceCall.query.filter_by(id=servicecall_id).first().serialize)

@sv.route('/',methods=["GET"])
def get_all_servicecall():
    return jsonify(data = [ i.serialize for i in ServiceCall.query.all()])



