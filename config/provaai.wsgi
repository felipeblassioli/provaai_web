import os
import site
from os.path import join,dirname,abspath

import sys
sys.stdout = sys.stderr

VENV_PACKAGES = join(dirname(abspath(__file__)), 'env/lib/python2.7/site-packages')
site.addsitedir(VENV_PACKAGES)

os.environ['PROVAAI_SETTINGS'] = '/var/www/provaai/provaai.cfg'
from provaai import app as application
