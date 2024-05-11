#! /usr/lib/python3.8

import logging
import sys
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/assettracking/')
activate_this = './venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
from project import create_app
app = create_app()#pplication.secret_key = 'abc123'
