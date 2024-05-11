#! /usr/lib/python3.8

import logging
import sys
import os
logging.basicConfig(stream=sys.stderr)
print("Version", sys.version)
print(sys.path)
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
sys.path.append(0, '/var/www/assettracking/')
from .project import create_app
app = create_app()#pplication.secret_key = 'abc123'
