#!/usr/bin/env python
""" Loads Question data into DataStore from AppEngine console
"""

import sys
from models import *
from lib.datastore.loader import load
from imported_question_data import DATA

options = dict(
    output = sys.stdout,
    cleanup = True,
    compressed = False,
    yaml_mark_subref = ':',
    yaml_data_header = '\n\nLoading data source: yaml, model: %(model)s, cleanup: %(cleanup)s\n\n',
    raw_data_format = '%s\n\n',
    raw_data_format_options = {'width': 80, 'depth': 7, 'indent': 2},
    model_instance_format = '%s\n\n',
    )
    
load(Question, DATA, **options)
