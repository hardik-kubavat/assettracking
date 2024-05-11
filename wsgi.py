import sys
import site

activate_this = './venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

#site.addsitedir('./venv/lib/python3.6/site-packages')
#sys.path.insert(0, '/var/www/html/southside/routing-webapp/project')

from project import create_app
app = create_app()


