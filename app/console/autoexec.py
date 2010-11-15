"""
This is the App Engine Console auto-executing module.  When you start a console session, it will
execute "from autoexec import *".  So you may place anything in here which you find useful.
"""

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users
import sys, os, logging

# import site help
import site
help = site._Helper()

# create fake webapp request
wsgienv = dict(os.environ)
wsgienv['wsgi.url_scheme'] = wsgienv['SERVER_PROTOCOL'].split('/', 1)[0].lower()
request = webapp.Request(wsgienv)

# import models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import *

