#!/usr/bin/env python

import sys

#from models import *
from lib.datastore.loader import *

NAME   = 'question'
SOURCE = 'x-%s-data.yaml' % NAME

ls(yamlfile=SOURCE, model=None)
