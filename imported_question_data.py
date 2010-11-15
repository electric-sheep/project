#!/usr/bin/env python
""" Question data
"""

COMPRESSED = True

if COMPRESSED:
    import bz2, base64
    unpack = lambda data: bz2.decompress(base64.decodestring(data))
else:
    unpack = lambda data: data

DATA = unpack('''QlpoOTFBWSZTWdw2BnIAACVfgAAQcAcgF6gABAo/597gIACUhKSTyRp7QUMJoyGnpqBqamTT1NqA
A0GgAZNoctjUMxisFy+LokHz64d3NVeBgpoqtBVnPTmxSwc8k9NowW3yzZBR09jtTF2vDEg+mdTd
CToIKsN6MubPOUUIOyiWhVqHKRKKI2dX9fdcMHwCxY2IdDX8QC6ZMrw6zF0ALUDkul/F3JFOFCQ3
DYGcgA==
''')
