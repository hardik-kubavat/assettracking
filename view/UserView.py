from flask import Blueprint,request,render_template, make_response, jsonify,redirect,url_for
from project.models.UserModel import User
from project import db,logger
import traceback

uv = Blueprint('user','user',url_prefix="/user")

@uv.route('/add',methods=['GET','POST'])
def addorupdate():
    if request.form and request.form.get('user_id') is '':
        logger.debug("User add operation is executing...")
        try:
            user = User(firstname=request.form.get('fname'),lastname=request.form.get('lname'),emailid=request.form.get("email"),password=request.form.get("pwd"),mobile=request.form.get("mobile"))
            db.session.add(user)
            db.session.commit()
            logger.debug("User added successfully. {0} {1}".format(user.id,request.form.get("email")))
            return make_response("success"),200
        except Exception as e:
            logger.error(str(e))
            return make_response(str(e)),500
    else:
        logger.debug("User {} - Update operation is executing... ".format(request.form.get('user_id')))
        try:
            user = User.query.filter_by(id=request.form.get('user_id')).first()
            user.setFirstName(request.form.get('fname'))
            user.setLastName(request.form.get('lname'))
            user.setEmailid(request.form.get("email"))
            user.setPassword(request.form.get("pwd"))
            user.setMobile(request.form.get("mobile"))
            db.session.commit()
            logger.debug("User {} - Updated successfully...".format(request.form.get('user_id')))
            return make_response("success"),200
        except Exception as e:
            logger.debug(str(e))
            return make_response(str(e)),500
    logger.debug("Add/Update data request is not recevied as form. Please Troubleshoot")
    return make_response("There is an error... Please check logs"),500

@uv.route('/delete/<user_id>')
def delete(user_id):
    logger.debug("User {} - Delete operation is executing. ".format(user_id))
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    logger.debug("User {} - Deleted Successfully.")
    return redirect(url_for("navigation.user"))

@uv.route('/get/<user_id>',methods=['GET'])
def get_user_by_id(user_id):
    return jsonify(User.query.filter_by(id=user_id).first().serialize)

@uv.route('/get_data')
def get_users_json():
    return jsonify(data = [ i.serialize for i in User.query.all()])

@uv.route('/createdb')
def createdb():
    try:
        db.create_all()
        db.session.commit()
    except:
        print("Error in creating database")
        traceback.print_exc(file=sys.stdout)
        return make_response("500")
    return make_response("200")

