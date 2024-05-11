#! /usr/lib/python3.8

import logging
import sys
import os
logging.basicConfig(stream=sys.stderr)
print("Version", sys.version)
print(sys.path)
sys.path.insert(0, '/var/www/assettracking/')
from .project import create_app
app = create_app()#pplication.secret_key = 'abc123'
