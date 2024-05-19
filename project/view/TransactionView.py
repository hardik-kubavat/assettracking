from flask import Blueprint,request,render_template, make_response, jsonify,redirect,url_for,send_file
from project.models.TransactionModel import Transaction
from project import logger
from project.extention import db
from project.models import TransactionModel,ProductModel

tv = Blueprint('transaction','transaction',url_prefix="/transaction")

@tv.route('/',methods=['POST'])
def allocate_transaction():
    if request.form:
        logger.debug("Allocate transcation operation is executing...")
        logger.debug(str(request.form))
        try:
            transaction = Transaction(product_id=request.form.get('product_id'),locater_id=request.form.get('locater_id'),remarks=request.form.get('remarks'))
            db.session.add(transaction)
            db.session.commit()
            logger.debug("Transaction added successfully. ")
            return make_response("Success"),200
        except Exception as e:
            logger.error(str(e))
            return make_response("Error while saving record. {}".format(str(e))),500
    
    logger.debug("Data request is not recevied as form. Please Troubleshoot")
    return make_response("There is an error... Please check logs"),500

@tv.route('/',methods=["GET"])
def get_all_transaction():
    return jsonify(data = [ i.serialize for i in TransactionModel.getAll()])

@tv.route('/replace',methods=['POST'])
def replace_asset_transaction():
    if request.form:
        logger.debug("Replace transaction operation is executing...")
        logger.debug(str(request.form))
        try:
            product_from = ProductModel.getById(request.form.get('product_from_id'))
            product_to = ProductModel.getById(request.form.get('product_to_id'))
            
            
            transaction1 = Transaction(product_id=product_from.id,locater_id=product_to.currentlocater_id,remarks=request.form.get('remarks'))
            transaction2 = Transaction(product_id=product_to.id,locater_id=product_from.currentlocater_id,remarks=request.form.get('remarks'))
            
            db.session.add(transaction1)
            db.session.add(transaction2)
            db.session.commit()
            logger.debug("Both Transactions added successfully. ")
            return make_response("Success"),200
        except Exception as e:
            logger.error(str(e))
            return make_response("Error while saving record. {}".format(str(e))),500
    
    logger.debug("Data request is not recevied as form. Please Troubleshoot")
    return make_response("There is an error... Please check logs"),500

@tv.route('/product/<product_id>',methods=["GET"])
def get_transaction_by_product(product_id):
    logger.debug(request.accept_mimetypes.accept_json)
    logger.debug(request.accept_mimetypes.accept_html)
    transactions = TransactionModel.getByProductId(product_id=product_id)
    logger.debug(transactions[0].product)
    if request.accept_mimetypes.accept_json :
        return jsonify(data = [ i.serialize for i in transactions])
    else:
        return render_template("showhistorytemplate.html",transactions=transactions,product=transactions[0].product)




