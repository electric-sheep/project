#!/usr/bin/env python

import sys

from models import *
from lib.datastore.loader import *

MODEL  = Question
NAME   = MODEL.__name__.lower()
SOURCE = 'x-%s-data.yaml' % NAME

ls(yamlfile=SOURCE, model=MODEL)
