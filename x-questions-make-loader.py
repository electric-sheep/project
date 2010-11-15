#!/usr/bin/env python

from __future__ import with_statement

from models import *
from lib.datastore.loader import *

MODEL  = Question
NAME   = MODEL.__name__.lower()
SOURCE = 'x-%s-data.yaml' % NAME
LOADER = 'x-%s-data-load.py' % NAME
PYDATA = 'imported_%s_data.py' % NAME

with file(LOADER, 'wb') as F:
    F.write(make_loader(MODEL, yamlfile=SOURCE, cleanup = True, pydata=PYDATA))

with file(PYDATA, 'wb') as F:
    F.write(make_pydata(MODEL, yamlfile=SOURCE))
