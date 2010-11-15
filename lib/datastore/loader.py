#!/usr/bin/env python
""" AppEngine DataStore loader
"""
__all__ = '''
    db 
    rm ls load make_loader make_pydata
    yaml_records
    UTF8_ALIASES 
    YAML_MARK_SUBREF
    YAML_FILE_HEADER YAML_DATA_HEADER DATASTORE_HEADER
    RAW_DATA_FORMAT RAW_DATA_FORMAT_OPTIONS MODEL_INSTANCE_FORMAT
    REMOVE_MESSAGE LOADER_MESSAGE
    LOADER_FORMAT LOADER_OPTIONS
    '''.split() 

import sys, os, yaml, bz2, base64
from cStringIO import StringIO
from pprint import PrettyPrinter

from google.appengine.ext import db, blobstore



UTF8_ALIASES = set('utf-8 utf_8 utf8 U8 UTF'.split())

YAML_MARK_SUBREF = ':'

YAML_FILE_HEADER = "\n\nData source: '%(yamlfile)s', model: %(model)s, encoding: %(encoding)s\n\n"
YAML_DATA_HEADER = "\n\nLoading data source: yaml, model: %(model)s, cleanup: %(cleanup)s\n\n"
DATASTORE_HEADER = "\n\nData source: datastore, model: %(model)s\n\n"

RAW_DATA_FORMAT  = "%s\n\n"
RAW_DATA_FORMAT_OPTIONS = dict(indent=2, width=80, depth=7)
MODEL_INSTANCE_FORMAT = "%s\n\n"

REMOVE_MESSAGE = "Removing all data from %(model)s\n"
LOADER_MESSAGE = "Creating loader for data source: '%(yamlfile)s', model: %(model)s, encoding: %(encoding)s\n"
PYDATA_MESSAGE = "Creating pydata for data source: '%(yamlfile)s', model: %(model)s, encoding: %(encoding)s\n"

LOADER_FORMAT = '''#!/usr/bin/env python
""" Loads %(model)s data into DataStore from AppEngine console
"""

import sys
from %(models_lib)s import *
from %(loader_lib)s import load
%(pydata_on)sfrom %(pydata_lib)s import DATA

options = dict(
    output = %(output)s,
    cleanup = %(cleanup)s,
    compressed = %(compressed)s,
    yaml_mark_subref = %(yaml_mark_subref)s,
    yaml_data_header = %(yaml_data_header)s,
    raw_data_format = %(raw_data_format)s,
    raw_data_format_options = %(raw_data_format_options)s,
    model_instance_format = %(model_instance_format)s,
    )
    
load(%(model)s, %(data)s, **options)
'''
LOADER_OPTIONS = dict(
    models_lib = 'models',
    loader_lib = 'lib.datastore.loader',
    output = 'sys.stdout',
    yaml_mark_subref = repr(YAML_MARK_SUBREF),
    yaml_data_header = repr(YAML_DATA_HEADER),
    raw_data_format = repr(RAW_DATA_FORMAT),
    raw_data_format_options = repr(RAW_DATA_FORMAT_OPTIONS),
    model_instance_format = repr(MODEL_INSTANCE_FORMAT),
    )

PYDATA_FORMAT = '''#!/usr/bin/env python
""" %(model)s data
"""

COMPRESSED = %(compressed)s

if COMPRESSED:
    import bz2, base64
    unpack = lambda data: bz2.decompress(base64.decodestring(data))
else:
    unpack = lambda data: data

DATA = unpack(%(data)s)
'''
PYDATA_OPTIONS = {}



def yaml_records(yamldata, encoding=None, yaml_mark_subref = YAML_MARK_SUBREF):
    """ Iterate over YAML data records

        * Any record fields named ':' or '::.*' are treated as dictionaries and used to update the record.
        * Any record fields named ':([^:].*)' are used to update '\1' field in the record .
    """
    yaml_mark_subref_len = yaml_mark_subref is not None and len(yaml_mark_subref) or 0

    if encoding and encoding not in UTF8_ALIASES: # UTF-8 is default encoding in YAML
        yamldata = yamldata.decode(encoding)

    for data in yaml.load_all(yamldata):
        if not isinstance(data, list):
            data = [data] # data may contain one record or list of records (used when sharing references)

        for d in data:
            if d is not None:
                if yaml_mark_subref_len:
                    for k in sorted(d):
                        if k.startswith(yaml_mark_subref):
                            sub = d.pop(k)
                            ref = k[yaml_mark_subref_len:]
                            if not ref or ref.startswith(yaml_mark_subref):
                                for sk in sub:
                                    if not sk in d:
                                        d[sk] = sub[sk]
                            elif ref in d:
                                pre = d[ref]
                                if isinstance(pre, list):
                                    assert isinstance(sub, list), "yaml sub reference '%s' requires a list: %r" % (ref, sub)
                                    pre.extend(sub)
                                elif isinstance(pre, basestring):
                                    assert isinstance(sub, basestring), "yaml sub reference '%s' requires a string: %r" % (ref, sub)
                                    d[ref] = '%s\n\n%s' % (pre.strip(), sub.strip())
                                else:
                                    for sk in sub:
                                        if not sk in pre:
                                            pre[sk] = sub[sk]
                            else:
                                d[ref] = sub
                yield d




def rm(*models, **options):
    """ Remove model data from DataStore

         * datastore access works server-side only
    """
    return __rm(models, **options)

def __rm(models, output=sys.stdout, remove_message = REMOVE_MESSAGE):
    if not output:
        output = StringIO()

    for m in models:
        if remove_message:
            output.write(remove_message % dict(model=m.__name__))
        db.delete(m.all(keys_only=True))

    return getattr(output, 'getvalue', lambda: None)() # output if stringio, or None


def ls(*models, **options):
    """ Output model data from DataStore, or from yaml file/data source

         * datastore access works server-side only
         * yaml file access works client-side only
         * encoding defaults to UTF-8 (YAML default)
         * if model name is provided, loaded yaml data are used to create its instances
    """
    return __ls(models, **options)

def __ls(models=None, yamldata=None, yamlfile=None, encoding=None, model=None,
    output = sys.stdout,
    yaml_mark_subref = YAML_MARK_SUBREF,
    yaml_file_header = YAML_FILE_HEADER,
    yaml_data_header = YAML_DATA_HEADER,
    datastore_header = DATASTORE_HEADER,
    raw_data_format = RAW_DATA_FORMAT,
    raw_data_format_options = None,
    model_instance_format = MODEL_INSTANCE_FORMAT,
    **options):

    if not output:
        output = StringIO()

    if yamldata is not None or yamlfile is not None:
        if raw_data_format_options is None:
            raw_data_format_options = dict(RAW_DATA_FORMAT_OPTIONS)
        if options:
            raw_data_format_options.update(options)
        raw_data_pp = PrettyPrinter(stream=output, **raw_data_format_options)

    if models is not None:
        for m in models:
            if datastore_header:
                output.write(datastore_header % dict(model=m.__name__))
            for i in m.all():
                if model_instance_format: output.write(model_instance_format % i)

    if yamldata is not None:
        if yaml_data_header:
            output.write(yaml_data_header % dict(model=model and model.__name__ or '-'))

	for d in yaml_records(yamldata, encoding=encoding, yaml_mark_subref=yaml_mark_subref):
            if raw_data_format: output.write(raw_data_format % raw_data_pp.pformat(d))
            if model:
                i = model(**d)
                if model_instance_format: output.write(model_instance_format % i)

    if yamlfile is not None:
        if yaml_file_header:
            output.write(yaml_file_header % dict(yamlfile=yamlfile, encoding=encoding,
                model=model and model.__name__ or '-'))

	for d in yaml_records(file(yamlfile).read(), encoding=encoding, yaml_mark_subref=yaml_mark_subref):
            if raw_data_format: output.write(raw_data_format % raw_data_pp.pformat(d))
            if model:
                i = model(**d)
                if model_instance_format: output.write(model_instance_format % i)

        # __ls(yamldata=file(yamlfile).read(), encoding=encoding, model=model, output=output
        #    yaml_mark_subref = yaml_mark_subref,
        #    yaml_data_header = '', # file header was output, skip data header
        #    raw_data_format = raw_data_format,
        #    raw_data_format_options = raw_data_format_options,
        #    model_instance_format = model_instance_format,
        #    )

    return getattr(output, 'getvalue', lambda: None)() # output if stringio, or None


def load(model, yamldata, cleanup=False, encoding=None, compressed=False,
    output = sys.stdout,
    yaml_mark_subref = YAML_MARK_SUBREF,
    yaml_data_header = YAML_DATA_HEADER,
    raw_data_format = RAW_DATA_FORMAT,
    raw_data_format_options = None,
    model_instance_format = MODEL_INSTANCE_FORMAT,
    **options):
    """ Loads model data from yaml data source into DataStore

         * datastore access works server-side only
         * encoding defaults to UTF-8
    """
    if not output:
        output = StringIO()

    if raw_data_format_options is None:
        raw_data_format_options = dict(RAW_DATA_FORMAT_OPTIONS)
    if options:
        raw_data_format_options.update(options)
    raw_data_pp = PrettyPrinter(stream=output, **raw_data_format_options)

    if yaml_data_header:
        output.write(yaml_data_header % dict(model=model.__name__, cleanup=cleanup))

    if cleanup:
        rm(model, remove_message='')

    if compressed:
        yamldata = bz2.decompress(base64.decodestring(yamldata))

    for d in yaml_records(yamldata, encoding=encoding, yaml_mark_subref=yaml_mark_subref):
        if raw_data_format: output.write(raw_data_format % raw_data_pp.pformat(d))
        i = model(**d)
        if model_instance_format: output.write(model_instance_format % i)
        i.put()

    return getattr(output, 'getvalue', lambda: None)() # output if stringio, or None

def make_loader(model, yamlfile, cleanup=False, encoding=None, dump=True, compressed=True,
    pydata = None,
    output = sys.stdout,
    data_row_sep = "'\n    '",
    loader_message = LOADER_MESSAGE,
    loader_format  = LOADER_FORMAT,
    loader_options = None,
    **options):
    """ Reads data from a local yaml file and outputs a loader code to be run in AppEngine console

         * encoding defaults to UTF-8
    """
    if not output:
        output = StringIO()

    if loader_message:
        output.write(loader_message % dict(
            yamlfile=yamlfile, model=model.__name__, encoding=encoding))

    if pydata:
        yamldata = 'DATA'
        pydata_lib = os.path.splitext(pydata)[0].replace(os.path.sep, '.')
        assert pydata_lib, 'unable to determine data module path for %r' % pydata

    else:
        yamldata = file(yamlfile).read()

        if encoding and encoding not in UTF8_ALIASES: # UTF-8 is default encoding in YAML
            yamldata = yamldata.decode(encoding)

        if dump:
            yamldata = yaml.dump_all(yaml.load_all(yamldata))

        if compressed:
            yamldata = "'''%s'''" % base64.encodestring(bz2.compress(yamldata))
        else:
            yamldata = repr(yamldata)
            data_row_sep = '\\n%s' % data_row_sep
            yamldata = data_row_sep.join(yamldata.split('\\n'))

    if loader_options is None:
        loader_options = dict(LOADER_OPTIONS)
    if options:
        loader_options.update(options)

    loader_options.update(
        data = yamldata,
        model = model.__name__,
        cleanup = cleanup,
        pydata_on = not pydata and '# ' or '',
        pydata_lib = pydata and pydata_lib or '<data_%s>' % model.__name__.lower(),
        compressed = compressed and not pydata,
        )

    return loader_format % loader_options

def make_pydata(model, yamlfile, encoding=None, dump=True, compressed=True,
    output = sys.stdout,
    pydata_message = PYDATA_MESSAGE,
    pydata_format  = PYDATA_FORMAT,
    pydata_options = None,
    **options):
    """ Reads data from a local yaml file and outputs a loader code to be run in AppEngine console

         * encoding defaults to UTF-8
    """
    if not output:
        output = StringIO()

    if pydata_message:
        output.write(pydata_message % dict(
            yamlfile=yamlfile, model=model.__name__, encoding=encoding))

    yamldata = file(yamlfile).read()

    if encoding and encoding not in UTF8_ALIASES: # UTF-8 is default encoding in YAML
        yamldata = yamldata.decode(encoding)

    if dump:
        yamldata = yaml.dump_all(yaml.load_all(yamldata))

    if compressed:
        yamldata = "'''%s'''" % base64.encodestring(bz2.compress(yamldata))
    else:
        yamldata = repr(yamldata)
        data_row_sep = '\\n%s' % data_row_sep
        yamldata = data_row_sep.join(yamldata.split('\\n'))

    if pydata_options is None:
        pydata_options = dict(PYDATA_OPTIONS)
    if options:
        pydata_options.update(options)

    pydata_options.update(
        data = yamldata,
        model = model.__name__,
        compressed = compressed,
        )

    return pydata_format % pydata_options




if __name__ == "__main__":
    import doctest
    doctest.testmod()
