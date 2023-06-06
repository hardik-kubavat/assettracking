#! /usr/lib/python3.8

import logging
import sys
logging.basicConfig(stream=sys.stderr)
print("Version", sys.version)
sys.path.insert(0, '/var/www/apps/assettracking/venv/lib/python3.8/site-packages')
sys.path.insert(0, '/var/www/apps/assettracking')
print(sys.path)
from base import app as application
application.secret_key = 'abc123'
