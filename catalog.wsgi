import sys
import os

PROJECT_DIR = '/var/www/fullstack/'
activate_venv = os.path.join(PROJECT_DIR, 'venv' , 'bin', 'activate_this.py')
execfile(activate_venv, dict(__file__=activate_venv))

sys.path.append(PROJECT_DIR)

from catalog import create_app
application = create_app('application.cfg')
