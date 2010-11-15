#!/usr/bin/env python
""" Electric Sheep at GUG Hackathon Prague 2010/11/15

    * https://github.com/electric-sheep
    * http://czu.gug.cz/search/label/hackathon
"""
import os, logging, re, string, random

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

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

SID_ALPHABET = string.digits + string.ascii_lowercase
SID_LEN = 32
SID_RE = '[a-z0-9]{32}'
UID_RE = '.+'
QID_RE = '[a-z0-9]{8}'
AID_RE = '[0-9]'

CT = 'Content-Type'
CT_HTML = 'text/html; charset=utf-8'
CT_JSON = 'application/json; charset=utf-8'




class Home(webapp.RequestHandler):
    def get(self):
        self.response.out.write(HOME_TEMPLATE)

class Login(webapp.RequestHandler):
    def post(self, nick):
        sid = ''.join(random.sample(SID_ALPHABET, SID_LEN))
        self.response.headers[CT] = CT_JSON
        json.dump(dict(session=sid), self.response.out)

class Question(webapp.RequestHandler):
    def post(self, sid):
	data = dict(
            question = 'What is the meaning of life, universe & everything?',
            token    = 'abcdefg8',
            answers  = 'blah doh 42 haha'.split(),
            ttl      =  4500,
            combatants = [
                dict(name='Honza', icon='http://img.twitter.com/9046.png', status=True, score=12345),
                ]
            )
        self.response.headers[CT] = CT_JSON
        json.dump(data, self.response.out)

class Answer(webapp.RequestHandler):
    def post(self, sid, qid, aid):
	data = dict(
            combatants = [
                dict(name='Honza', icon='http://img.twitter.com/9046.png', status=True, score=12345),
                ]
            )
        self.response.headers[CT] = CT_JSON
        json.dump(data, self.response.out)




if DEBUG_MODE:
    for handler in (Login, Question, Answer):
        def debug_get(self, *args):
            self.post(*args)
            self.response.headers[CT] = CT_HTML

        handler.get = debug_get # allow debugging via get requests

application = webapp.WSGIApplication([
    (r'/', Home),
    (r'/login/(%s)' % UID_RE, Login),
    (r'/question/(%s)' % SID_RE, Question),
    (r'/answer/(%s)/(%s)/(%s)' % (SID_RE, QID_RE, AID_RE), Answer),
    ],
    debug = DEBUG_MODE)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()