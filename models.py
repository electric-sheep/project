#!/usr/bin/env python
""" Data models
"""
__all__ = 'Session Question'.split()

import logging, string, random

from google.appengine.ext import db
from google.appengine.api import memcache

class Session(db.Model):
    SID_ALPHABET = string.digits + string.ascii_lowercase
    SID_LEN = 32
    SID_RE = '[a-z0-9]{32}'
    UID_RE = '.+'
    
    sid = db.StringProperty(required=True)
    uid = db.StringProperty(required=True)
    score = db.IntegerProperty(required=True, default=0)
    ctime = db.DateTimeProperty(required=True, auto_now_add=True)
    atime = db.DateTimeProperty(required=True, auto_now_add=True)

    def __init__(self, *args, **argd):
        if not 'sid' in argd:
            argd['sid'] = ''.join(random.sample(self.SID_ALPHABET, self.SID_LEN))

        super(Session, self).__init__(*args, **argd)

class Question(db.Model):
    QID_ALPHABET = string.digits + string.ascii_lowercase
    QID_LEN = 8
    QID_RE = '[a-z0-9]{8}'
    AID_RE = '[0-9]'

    qid  = db.StringProperty(required=True)
    next = db.StringProperty(required=True)

    text = db.StringProperty(required=True, indexed=False)

    answer = db.IntegerProperty(required=True, indexed=False)
    answers = db.ListProperty(unicode, required=True, indexed=False)

    def __init__(self, *args, **argd):
        qid = argd.get('qid', None)
        if qid is None:
            argd['qid'] = qid = ''.join(random.sample(self.QID_ALPHABET, self.QID_LEN))

        argd['answers'] = map(unicode, argd['answers'])

        status = Status.get()
        if status is None:
            Status.initialize(qid)
            logging.info('question add: %s ' % (qid))
            argd['next'] = qid
        else:
            logging.info('question add: %s -> %s -> %s' % (status.last, qid, status.first))
            last = Question.all().filter('qid', status.last).get()
            last.next = qid
            last.put()
            Status.update(last=qid)
            argd['next'] = status.first

        super(Question, self).__init__(*args, **argd)




class Status(db.Model):
    ANSWER_TIMEOUT = 10 + 1
    ATTRS = 'first last current opened'.split()

    first = db.StringProperty(required=True)
    last  = db.StringProperty(required=True)
    current = db.StringProperty()
    opened = db.DateTimeProperty()

    @classmethod
    def get(cls):
        status = memcache.get(cls.__name__)
        if status is not None:
            return cls(**status)
        else:
            status = cls.all().get()
            if status is not None:
                data = status.data
                logging.info('memcache add: %s: %r' % (cls.__name__, data))
                if status is not None and not memcache.add(cls.__name__, data):
                    logging.error('memcache add failed: %s: %r' % (cls.__name__, data))
            return status

    @classmethod
    def set(cls, **data):
        status = cls(**data)
        status.put()
        logging.info('memcache set: %s: %r' % (cls.__name__, data))
        if not memcache.set(cls.__name__, data):
            logging.error('memcache set failed: %s: %r' % (cls.__name__, data))
        return status

    @classmethod
    def initialize(cls, qid):
        cls.set(first=qid, last=qid)

    @classmethod
    def update(cls, **data):
        status = cls.get()
        assert status is not None, '%s update requires defined status' % cls.__name__

        updated = False
        for attr in data:
            if getattr(status, attr) != data:
                updated = True
                setattr(status, attr, data)

        if updated:
            status.put()
            data = status.data
            logging.info('memcache set: %s update: %r' % (cls.__name__, data))
            if not memcache.set(cls.__name__, data):
                logging.error('memcache set failed: %s update: %r' % (cls.__name__, data))

        return updated

    @property
    def data(self):
        return dict((attr, getattr(self, attr)) for attr in self.ATTRS)



