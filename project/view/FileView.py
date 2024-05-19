import os
import glob
from flask import Blueprint, jsonify, render_template
from datetime import datetime

comv = Blueprint('Common','Common',url_prefix="/utils")

def get_backup_status(file):
    modified_date = datetime.fromtimestamp(os.path.getmtime(file))
    difference = datetime.now() - modified_date
    if difference.days > 2:
        return "ERROR"
    return "SUCCESS"


@comv.route('/listfiles',methods=['GET','POST'])
def addorupdate():
    root_directory = "/home/bkp_server/backup/"
    files_list= []
    for subdir, dirs, files in os.walk(root_directory):
        if 'db' in subdir:
            list_of_files = glob.glob(subdir+'/*')
            latest_file = max(list_of_files, key=os.path.getctime)
            files_list.append(latest_file)

    
    file_status = dict()
    for file in files_list:
        file_status[file.split('/')[-3].title()] = (datetime.fromtimestamp(os.path.getmtime(file)).strftime("%d-%m-%Y %H:%M"), file.split('/')[-3].title(), os.path.basename(file).split('/')[-1], get_backup_status(file))
    return render_template("dashboard.html", backup_status=file_status)
