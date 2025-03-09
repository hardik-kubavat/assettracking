from flask import Blueprint, request, make_response, jsonify, redirect, url_for
from project.models.PurchaseOrdersModel import PurchaseOrder
from project.models import PurchaseOrdersModel
from project import logger
from project.extention import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime

pov = Blueprint('PurchaseOrder', 'PurchaseOrder', url_prefix="/purchaseorder")

# Helper function to save the uploaded file
def save_po_file(po_file):
    project_root = os.path.abspath(os.path.dirname(__file__))
    upload_folder = os.path.join(project_root,'..' ,'static', 'uploads', 'po_files')
    logger.error("Upload Folder Path : ", upload_folder)
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(po_file.filename)
    file_path = os.path.join(upload_folder, filename)
    po_file.save(file_path)
    return filename

@pov.route('/add', methods=['POST'])
def add_or_update():
    if request.form and request.form.get('po_id') == '':
        # Add operation
        logger.debug("Purchase Order add operation is executing...")
        try:
            po_number = request.form.get('po_number')
            po_date = request.form.get('po_date')
            po_title = request.form.get('po_title')
            delivery_date = request.form.get('delivery_date', None)
            warranty_ends = request.form.get('warranty_ends', None) 
            deadstock_date = request.form.get('deadstock_date', None) 
            description = request.form.get('description')

            # Handle file upload
            po_file = request.files.get('po_file')
            print("PO FILE", request.files)
            po_filename = save_po_file(po_file) if po_file else None

            # Create new purchase order
            purchase_order = PurchaseOrder(po_number=po_number, po_title=po_title,
                                                 po_date=po_date,
                                                 delivery_date=delivery_date  if delivery_date != "" else None,
                                                 warranty_ends=warranty_ends if warranty_ends != "" else None,deadstock_date=deadstock_date if deadstock_date != "" else None,isdeleted=False,description=description,po_file=po_filename)
            db.session.add(purchase_order)
            db.session.commit()
            logger.debug(f"Purchase Order {po_number} added successfully.")
            return make_response("success"), 200
        except Exception as e:
            logger.error(str(e))
            return make_response(str(e)), 500
    else:
        # Update operation
        logger.debug(f"Purchase Order {request.form.get('po_id')} - Update operation is executing...")
        try:
            po_id = request.form.get('po_id')
            purchase_order = PurchaseOrdersModel.getById(po_id)

            purchase_order.setPoNumber(request.form.get('po_number'))
            purchase_order.setPoTitle(request.form.get('po_title'))
            purchase_order.setPoDate(request.form.get('po_date'))
            purchase_order.setDeliveryDate(request.form.get('delivery_date'))
            warranty_ends = request.form.get('warranty_ends', None)
            warranty_ends=warranty_ends if warranty_ends != "" else None
            purchase_order.setWarrantyEnds(warranty_ends)
            deadstock_date = request.form.get('deadstock_date', None)
            deadstock_date=deadstock_date if deadstock_date != "" else None
            purchase_order.setDeadstockDate(deadstock_date)
            purchase_order.setDescription(request.form.get('description'))

            # Handle file upload
            po_file = request.files.get('po_file')
            if po_file:
                purchase_order.setPoFile(save_po_file(po_file))

            db.session.commit()
            logger.debug(f"Purchase Order {po_id} updated successfully.")
            return make_response("success"), 200
        except Exception as e:
            logger.error(str(e))
            return make_response(str(e)), 500

@pov.route('/delete/<po_id>')
def delete(po_id):
    logger.debug(f"Purchase Order {po_id} - Delete operation is executing...")
    try:
        purchase_order = PurchaseOrdersModel.getById(po_id)
        db.session.delete(purchase_order)
        db.session.commit()
        logger.debug(f"Purchase Order {po_id} - Deleted successfully.")
        return redirect(url_for("navigation.po"))
    except Exception as e:
        logger.error(str(e))
        return make_response(str(e)), 500

@pov.route('/get/<po_id>', methods=['GET'])
def get_purchase_order_by_id(po_id):
    try:
        purchase_order = PurchaseOrdersModel.getById(po_id)
        return jsonify(purchase_order.serialize), 200
    except Exception as e:
        logger.error(str(e))
        return make_response("Error fetching the purchase order"), 500

@pov.route('/get_data')
def get_all_purchase_orders():
    try:
        purchase_orders = PurchaseOrdersModel.getAll()
        return jsonify(data=[po.serialize for po in purchase_orders]), 200
    except Exception as e:
        logger.error(str(e))
        return make_response("Error fetching purchase orders"), 500
    

# Add more routes if you want to include related data like categories for Purchase Orders
# @po.route('/<po_id>/categories', methods=['GET'])
# def get_categories_by_purchase_order(po_id):
#     return jsonify([category.serialize for category in getById(po_id).categories]), 200
