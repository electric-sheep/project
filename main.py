#!/usr/bin/env python
""" Electric Sheep at GUG Hackathon Prague 2010/11/15

    * https://github.com/electric-sheep
    * http://czu.gug.cz/search/label/hackathon
"""
import os, logging

from datetime import datetime

from models import *

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db

from google.appengine.api import memcache

try:
    import json
except ImportError:
    from django.utils import simplejson as json




DEBUG_MODE = os.environ.get('SERVER_SOFTWARE', '').lower().startswith('development')

if DEBUG_MODE:
    logging.root.setLevel(logging.DEBUG)

logging.info('initializing application %(APPLICATION_ID)s %(CURRENT_VERSION_ID)s on %(HTTP_HOST)s (%(SERVER_SOFTWARE)s)'
    % os.environ)

TEMPLATES = os.path.dirname(__file__)

HOME_TEMPLATE = file(os.path.join(TEMPLATES, 'index.html')).read()

CT = 'Content-Type'
CT_HTML = 'text/html; charset=utf-8'
CT_JSON = 'application/json; charset=utf-8'




class Home(webapp.RequestHandler):
    def get(self):
        self.response.out.write(HOME_TEMPLATE)

class Login(webapp.RequestHandler):
    def post(self, uid):
        self.response.headers[CT] = CT_JSON

        S = Session(uid=uid)
        S.put()

        json.dump(dict(session=S.sid), self.response.out)

class GetQuestion(webapp.RequestHandler):
    def post(self, sid):
        self.response.headers[CT] = CT_JSON

        status = Status.get()
        now = datetime.now()

        if status.opened is None:
            status.update(opened=now, current=status.first)

        elif status.opened.toordinal() + status.ANSWER_TIMEOUT < now.toordinal():
            current = Question.all().filter('qid', status.current).get()
            status.update(opened=now, current=current.next)

        else:
            current = Question.all().filter('qid', status.current).get()

	data = dict(
            question = current.text,
            token    = current.qid,
            answers  = current.answers,
            ttl      = status.opened.toordinal() + status.ANSWER_TIMEOUT - now.toordinal(),
            combatants = [
                dict(name = s.uid, icon=None, status=None)
                for s in list(Session.all())
                ]
            )

        json.dump(data, self.response.out)

class PostAnswer(webapp.RequestHandler):
    def post(self, sid, qid, aid):
        self.response.headers[CT] = CT_JSON

	data = dict(
            combatants = [
                dict(name = s.uid, icon=None, status=None)
                for s in list(Session.all())
                ]
            )

        json.dump(data, self.response.out)




if DEBUG_MODE:
    for handler in (Login, GetQuestion, PostAnswer):
        def debug_get(self, *args):
            self.post(*args)
            self.response.headers[CT] = CT_HTML

        handler.get = debug_get # allow debugging via get requests

application = webapp.WSGIApplication([
    (r'/', Home),
    (r'/login/(%s)' % Session.UID_RE, Login),
    (r'/question/(%s)' % Session.SID_RE, GetQuestion),
    (r'/answer/(%s)/(%s)/(%s)' % (Session.SID_RE, Question.QID_RE, Question.AID_RE), PostAnswer),
    ],
    debug = DEBUG_MODE)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()